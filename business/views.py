import imp
from django.shortcuts import render,redirect
from django.urls import reverse
from django.contrib import messages
from .forms import LineForm,BankForm,DaysOpenForm,RemoveForm,JoinLineForm,EditLineForm,BusinessMenuForm
from account.forms import ChangePasswordForm,DeleteBusinessLineForm
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse,Http404
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from random import choice
from business.models import BusinessQueue,Item,Order
from users.models import UserQueue
from account.models import BusinessProfile
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime,timedelta
from django.utils import timezone 
from django.contrib.auth import login
import pytz,json,ast,requests
from django.core.paginator import Paginator
from users.signals import line_changed,notify,confirm_bank
from django.db import IntegrityError
from .forms import BANK_CHOICES as bank_list,RefundForm
from standing.settings import PAYSTACK_SCRET_KEY
from django.db.models import Q
from django.db import transaction
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from account.tokens import account_activation_token_two
from django.core.mail import send_mail
from django.template import loader
from django.contrib.auth.models import User
 


def confirm_business_signup_object(business):
    try:
        business = business.business_signup
        return business
    except Exception:
        return HttpResponseRedirect(reverse('login'))


# def confirm_business_exists(business_key):
#     try:
#         business = Business_signup.objects.get(key=business_key)
#         return business
#     except Exception:
#         messages.error(request, 'Business does not exist')
#         return HttpResponseRedirect(reverse('login'))

@login_required
def BusinessHomePageView(request):
    business = confirm_business_signup_object(request.user)
    businesslines = Business_line.objects.filter(business=business).order_by('name')
    first_letter = business.name[0].upper()
    
    return render(request,
                  'business/homepage/managebusinesspage.html',
                  {'businesslines': businesslines,
                   'business':business,
                   'first_letter':first_letter,
                   })
    



            
@login_required
def ItemsView(request):
    business = confirm_business_signup_object(request.user)
    items = business.all_items.all()
    if request.method =='GET':
        form = BusinessMenuForm()
        return render(request,'business/order/items.html',
                     {'items': items,
                      'form':form})
    
    if request.method =='POST':
        form = BusinessMenuForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            name = cd['name']
            item_exists = Items.objects.filter(name=name,business=business).exists()
            if item_exists:
                form.add_error('name','An item with this name already exists')
                return render(request,'business/order/items.html',
                     {'items': items,
                      'form':form})
            else:
                instance = Items(name=name)
                
                instance.business = business
                instance.price = cd['price']
                instance.units_available = cd['units_available']
                instance.save()
                messages.success(request,'Item added successfully')
                form = BusinessMenuForm()
                return render(request,'business/order/items.html',
                     {'items': items,
                      'form':form})
        else:
            return render(request,'business/order/items.html',
                     {'items': items,
                      'form':form})

            



@login_required
def EditItemView(request,identity):
    business = confirm_business_signup_object(request.user)
    if request.method =='POST':
        form = BusinessMenuForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            name = cd['name']
            present_item = Items.objects.get(id=identity)
            item_check = Items.objects.filter(name=name,business=business)
            item_exists = item_check.exists()
            if item_exists and (not present_item.name == item_check[0].name):
                form.add_error('name','An item with this name already exists')
                return render(request,'business/order/edit_item.html',
                     {'form': form,
                      'item':item})
            else:
                instance = present_item
                instance.name = name
                instance.business = business
                instance.price = cd['price']
                instance.units_available = cd['units_available']
                instance.save()
                messages.success(request,'Item updated successfully')
                form = BusinessMenuForm()
                return HttpResponseRedirect(reverse('business:items'))
        else:
            return render(request,'business/order/edit_item.html',
                     {'form': form,
                      'item':item })
    else:
        try:
            item = Items.objects.get(id=identity)
        except Exception:
            return HttpResponseRedirect(reverse('business:items'))
        data = {'name':item.name,
                'price':item.price,
                'units_available':item.units_available}
        form = BusinessMenuForm(initial=data)
        return render(request,'business/order/edit_item.html',
                     {'form': form,
                      'item':item})
            



@login_required
def OrdersView(request):
    business = confirm_business_signup_object(request.user)
    orders = Orders.objects.filter(business=business,status='PAID').order_by('-id')
    if request.GET.get('api',False)=='check':
        
        if business.has_orders:
            return HttpResponse('y')
        else:
            return HttpResponse('n')
    find = request.GET.get('find',False)
    if find:
        if ' ' in find:
            find = find.split(' ')
            orders = orders.filter((Q(user__first_name__icontains=find[0])
                                & Q(user__last_name__icontains=find[1]))
                                |(Q(user__first_name__icontains=find[1])
                                & Q(user__last_name__icontains=find[0]))
                                
                                )[:10]
        else:
            orders = orders.filter(Q(user__first_name__icontains=find)
                                |Q(user__last_name__icontains=find)
                                |Q(reference__icontains=find))[:10]
        new_obj = {}
        i=0
        if not orders:
            return HttpResponse('0')
        for all_ in orders:
            new_obj[i]=[all_.id,
                        all_.user.first_name+' '+all_.user.last_name,
                        all_.reference]
            i+=1
        return HttpResponse(JsonResponse(new_obj))
        
            
            
                                
                                   
    if business.has_orders:
        # incase the page is reloaded when a new one comes in
        messages.success(request,'You have new order(s)')
        business.has_orders= False
        business.save()
    status = request.GET.get('status',False)
    if status:
        if status == 'delivered':
            orders = orders.filter(order_status='COLLECTED')
        elif status == 'not ready':
            orders = orders.filter(order_status='SENT')
        elif status == 'ready':
            orders = orders.filter(order_status='READY')

            
    paginator = Paginator(orders, 50)
    page_number = request.GET.get('page')
    orders = paginator.get_page(page_number)
    return render(request,'business/order/orders.html',
                     {'orders': orders })

@login_required
def OrderDetailView(request,identity):
    business = confirm_business_signup_object(request.user)
    if identity=='find':
        try:
            order = Orders.objects.get(id=request.GET.get('ref'))
        except Exception:
            return HttpResponse('Something went wrong')
    else:
        try:
            order = Orders.objects.get(id=identity)
        except Exception:
            return HttpResponse('Something went wrong')

        
    if request.method == 'GET':
        if order.business != business:
            return HttpResponseRedirect(reverse('login'))
        ready = request.GET.get('p',False)
        if ready=='makeaware':
            notify.send(sender=None,
                        key=order.id,
                        collected=False,
                        request=request)
            return HttpResponse('good')
        check_pin = request.GET.get('pin',False)
        if check_pin:
            try:
                check_pin = int(check_pin)
            except ValueError:
                return HttpResponse('bad')
            if order.order_status == 'READY':
                if check_pin == order.pin:
                    notify.send(sender=None,
                            key=order.id,
                            collected=True)
                    return HttpResponse('good')
                else:
                    return HttpResponse('bad')
            else:
                return HttpResponse('reload')
            
            
        zone = pytz.timezone(business.timezone)
        created_date = timezone.localtime(order.created,zone)
        items = ast.literal_eval(order.items)
        customer = order.user
        form = RefundForm()
        return render(request,'business/order/order_detail.html',
                     {'order': order,
                      'items':items,
                      'refund_form':form,
                      'created_date':created_date,
                      'customer':customer})

    
    else:
        zone = pytz.timezone(business.timezone)
        created_date = timezone.localtime(order.created,zone)
        items = ast.literal_eval(order.items)
        customer = order.user
        form = RefundForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            checker = user.check_password(cd['password'])
            if not checker:
                form.add_error('password','incorrect password')
            else:
                if order.is_active:
                    if order.order_status =='SENT' or order.order_status =='READY':
                        order.order_status = 'REFUND REQUESTED'
                        order.save()
        return render(request,'business/order/order_detail.html',
                     {'order': order,
                      'items':items,
                      'refund_form':form,
                      'created_date':created_date,
                      'customer':customer})
            
    


                    
        
@login_required
def PaymentView(request):
    business = confirm_business_signup_object(request.user)
    if request.method=='POST':
        def get_bank_name(code):
            for all_ in range(len(bank_list)):
                if bank_list[all_][0]==code:
                    return bank_list[all_][1]

        form = BankForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            r_data = requests.get(
                    'https://api.paystack.co/bank/resolve',
                    headers={'Authorization': 'Bearer '+PAYSTACK_SCRET_KEY},
                    params={'account_number':cd['account_number'],
                            'bank_code':cd['bank']})
            r_data = r_data.json()
            print(r_data)
            if r_data['status']==True:
                transfer_recipient = requests.post(
                        'https://api.paystack.co/transferrecipient',
                        headers={'Authorization': 'Bearer '+ PAYSTACK_SCRET_KEY,
                                 'Content-Type': 'application/json'},
                        json={'type':'nuban',
                              'account_number':cd['account_number'],
                              'name':business.name,
                              'bank_code': cd['bank'],
                              'currency':"NGN"}
                        )
                transfer_recipient = transfer_recipient.json()
                print(transfer_recipient)
                if transfer_recipient['status']==True:
                    business.recipient_info = transfer_recipient['data']['recipient_code']
                    business.account_number = cd['account_number']
                    business.bank = get_bank_name(cd['bank'])
                    business.bank_account_name = r_data['data']['account_name']
                    business.order_active= True
                    business.bank_email_confirmation = False
                    business.save()
                    iioo = request.user#this is how it works
                    confirm_bank.send(sender=None,
                                      request=request,
                                      user = iioo)
                    return render(request,'business/order/payment.html',
                             {'form': form,
                              'business':business})
                else:
                    messages.error('Something went wrong')
                    return render(request,'business/order/payment.html',
                             {'form': form,
                              'business':business})
            else:
                form.add_error('account_number','Invalid account information')
                return render(request,'business/order/payment.html',
                             {'form': form,
                              'business':business})
    else:
        form = BankForm()
        return render(request,'business/order/payment.html',
                     {'form': form,
                      'business':business})


def activateBankView(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token_two.check_token(user, token):
        business = user.business_signup
        business.bank_email_confirmation = True
        business.save()
        messages.success(request,'Bank account information updated successfully')
        return HttpResponseRedirect(reverse('business:payment'))
    else:
        return HttpResponse('This link has expired')
        


def ResendConfirmationView(request):
    business = confirm_business_signup_object(request.user)
    if request.method=='GET':
        if not business.bank_email_confirmation:
            confirm_bank.send(sender=None,user=user,request=request)
            return HttpResponse('good')
        else:
            return HttpResponse('good')
    return HttpResponse('bad')








@login_required
def DelPaymentView(request):
    business = confirm_business_signup_object(request.user)
    GET =  request.GET.get('id',False)
    
    disable = request.GET.get('disable',False)
    if disable:
        if disable=='true':
            business.order_active = False
            business.save()
            return HttpResponse('disabled')
        elif disable=='false':
            business.order_active = True
            business.save()
            return HttpResponse('enabled')
        else:
            return HttpResponse('Something isn\'t right')
    if GET:
        try:
            item = Items.objects.get(id=GET)
            item.delete()
            messages.success(request,'Item removed successfully')
            return HttpResponseRedirect(reverse('business:items'))
        except Exception:
            messages.error(request,'Something went wrong')
            return HttpResponseRedirect(reverse('business:items'))
    if business.account_number:
        business.account_number = ""
        business.bank = ""
        business.bank_account_name = ''
        business.recipient_info = ""
        business.bank_email_confirmation = False
        business.save()
    messages.success(request,'Payment information deleted')
    return HttpResponseRedirect(reverse('business:payment'))





@login_required
def CreateLineView(request):
    user = confirm_business_signup_object(request.user)
    counting = user.business_line.all().count()
    if counting == 20:
        messages.error(request,
                             'Sorry, a business can only have 20 lines. Please delete an existing line to continue.')     
        return HttpResponseRedirect(reverse('business:business_homepage'))
    if request.method == 'POST':
        def randomticket():
            a = ['A','B','C','D','E','F','G','H',
                 'I','J','K','L','M','N','P',
                 'Q','R','S','T','U','V','W','X',
                 'Y','Z','a','b','c','d','e','f',
                 'g','h','i','j','k','m','n',
                 'p','q','r','s','t','u','v',
                 'w','x','y','z','2','3','4',
                 '5','6','7','8','9']
            #no 0,o,O,1,l to avoid confusion
            # all business unique keys must be 7
            # for the join by key operation
            return ( choice(a) + choice(a) 
                    +choice(a) + choice(a) 
                    +choice(a) + choice(a)
                    +choice(a))
        form = LineForm(request.user,request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            uniquefield = ''
            while True:
                uniquefield = randomticket()
                if not Business_line.objects.filter(uniquefield=uniquefield).exists():
                    break
            
            
            line_object = Business_line(name=cd['name'],
                                         information=cd['information'],
                                         instruction=cd['instruction'],
                                         uniquefield=uniquefield,
                                         business=user
                                         )
         
            while True:
                try:
                    line_object.save()
                    break
                except IntegrityError:
                    while True:
                        uniquefield = randomticket()
                        if not Special_line.objects.filter(uniquefield=uniquefield).exists():
                            break
                        line_object.uniquefield = uniquefield
            
            
            
            return HttpResponseRedirect(reverse('business:business_homepage'))
           
        else:
            return render(request, 'business/homepage/homepage.html',{'form':form})
        
    else:
        form = LineForm(request.user)
        return render(request, 'business/homepage/homepage.html',{'form':form})

@login_required
def EditLineView(request, slug):
    slug = slug  
    user = confirm_business_signup_object(request.user)
    line = Business_line.objects.get(business=user,slug=slug)
    if request.method == 'POST':
        form = EditLineForm(request.user,line,request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            line.name = cd['name']
            line.information = cd['information']
            line.instruction =  cd['instruction']
            line.save()
            messages.success(request,'Line information updated successfully')
            return HttpResponseRedirect (reverse('business:business_homepage'))
        else:
            return render(request,'business/homepage/edit_line.html',
                          {'form':form,
                           'line':line})
    else:
        
        form_data = {'name': line.name,
                'information':line.information,
                'instruction':line.instruction}

        
        
    
        form = EditLineForm(request.user,line,initial=form_data)
        delete_line_form = DeleteBusinessLineForm({'delete':line.uniquefield})
        return render(request,'business/homepage/edit_line.html',
                          {'form':form,
                           'delete_line_form':delete_line_form,
                           'line':line})
        


@login_required
def DaysOpenView(request):
    line = confirm_business_signup_object(request.user)
    user = line
    if request.method == 'POST':
        form = DaysOpenForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            today = timezone.now()
            zone = pytz.timezone(user.timezone)
            today = timezone.localtime(today,zone)
            d_o_w = ['monday','tuesday',
                   'wednesday','thursday',
                   'friday','saturday','sunday']
            c_d_o_w = d_o_w[:]
            for days in d_o_w:
                if cd[days] == False:
                    d_o_w.remove(days)
            for days in d_o_w[:]:
                if cd[days] == False:
                    d_o_w.remove(days)
            error = False
            for days in c_d_o_w:
                x = cd[days[:2]+'_o']
                y = cd[days[:2]+'_c']
                if (x and y ) and x > y and (days in d_o_w):
                    form.add_error(days[:2]+'_o','Business can not close before it opens')
                    error=True
                    
                if ((x and not y) or (y and not x)) and (days in d_o_w):
                    form.add_error(days[:2]+'_o',
                                   'Both opening and closing time should be provided')
                    error = True
            
                if cd[days] and (not x and not y):
                    form.add_error(days[:2]+'_o',
                                   'Time input must be added or '+days.upper() +' box should be unchecked')
                    error=True
                if x==y and (x and y):
                    form.add_error(days[:2]+'_o',
                                   'Sorry, opening and closing time can not be the same')
                    error=True
                    
            if error:
                return render(request,'business/homepage/business_hours.html',
                          {'form':form,
                           'line':line})
            days_open = []
            
            def get_x(var_x):
                o_c  = datetime(today.year,
                                     today.month,
                                     today.day,
                                     var_x.hour,
                                     var_x.minute,
                                     var_x.second,
                                    )
                o_c  = zone.normalize(zone.localize(o_c))
                o_c  = timezone.localtime(o_c)
                return o_c.time()

            the_list = ["monday","tuesday","wednesday",
                        "thursday","friday","saturday","sunday"]
            for each in the_list:
                if each in d_o_w:
                    d_o = each[:2]+"_o"
                    d_c = each[:2]+"_c"
                    exec_string_open = "line."+d_o+"= get_x(cd['"+str(d_o)+"'])"
                    exec_string_close = "line."+d_c+"= get_x(cd['"+str(d_c)+"'])"
                    exec(exec_string_open)
                    exec(exec_string_close)
                    days_open.append(each[:2])

            
            
            line.days_open = str(days_open)
            line.save()
            messages.success(request,'Business hours updated successfully')
            return HttpResponseRedirect (reverse('business:business_homepage'))
        else:
            
            return render(request,'business/homepage/business_hours.html',
                          {'form':form,
                           'line':line})
    else:
        zone = pytz.timezone(user.timezone)
        today = timezone.now()    
        today = timezone.localtime(today,zone)
        days_open = line.days_open
        if days_open:
            days_open = ast.literal_eval(days_open)
        else:
            days_open=[]
        form_data = {}

        
        def find_date(weekdayy,o_c):
            wikd = today.isoweekday()
            all_days = {'mo':1,'tu':2,'we':3,'th':4,'fr':5,'sa':6,'su':7}
            thedatetime = datetime(
                                  today.year,
                                  today.month,
                                  today.day,
                                  o_c.hour,
                                  o_c.minute)
            if all_days[weekdayy] >= wikd:
                variabu = all_days[weekdayy] - wikd
            else:
                variabu = (7 - all_days[weekdayy]) + wikd
        
            a_i = thedatetime + timedelta(days=variabu)
            a_i = timezone.localtime(timezone.make_aware(a_i),zone).time()
            return a_i

        date_obj = {'mo':'monday','tu':'tuesday','we':'wednesday','th':'thursday',
                    'fr':'friday','sa':'saturday','su':'sunday'}
        for short,full in date_obj.items():
            if short in days_open:
                form_data[full] = True
                form_data[short+"_o"] = find_date(short,eval("line"+"."+short+"_o"))
                form_data[short+"_c"] = find_date(short,eval("line"+"."+short+"_c"))

    
        form = DaysOpenForm(initial=form_data)
        return render(request,'business/homepage/business_hours.html',
                          {'form':form,
                           'line':line})
        





def business_ajax(request,uniquefield):
    user = request.user
    unique = uniquefield
    if not user.is_authenticated:
        return HttpResponse('a')
    try:   
        business = user.business_signup
    except ObjectDoesNotExist:
        return HttpResponse('a')
    line_object = False
    for all_ in business.business_line.all():
        if unique == all_.uniquefield:
            line_object = all_
    if not line_object:
        return HttpResponse('r')
    else:
        line = line_object.people_present.all().order_by('time')
    compare = request.session.get('compare', None)
    json_line={}
    if line:
        i=1
        number_of_people = len(line)
        for people in line:
            p_f_n = people.first_name
            if len(p_f_n) > 15:
                p_f_n = p_f_n[:15] + '...'
            json_line[str(i)] = p_f_n.title() +','+people.ticket+','+people.unique
            i += 1
            if i == 6:
                break
        json_line[6] = str(number_of_people)
        if compare:
            compare_list = list(compare.values())
            json_list = list(json_line.values())
            copy_compare = compare_list[:]
            copy_json = json_list[:]
            x = copy_compare.pop(-1)
            y = copy_json.pop(-1)
                        
            #if only number of people in line change
            if compare_list[:len(compare_list)-1] == json_list[:len(json_list)-1]:
                if x != y:
                    request.session['compare'] = json_line
                    return HttpResponse('*'+y)
            if compare_list == json_list:
                return HttpResponse('-')
        request.session['compare'] = json_line
        return HttpResponse(JsonResponse(json_line))
    else:
        if compare:
            request.session['compare'] = ''
            return HttpResponse(0)
        else:
            return HttpResponse(0)
            
    
@login_required
def LineDetailView(request,slug):
    slug=slug
    user = request.user
    thebusiness = confirm_business_signup_object(user)
    try:
        businessline = Business_line.objects.get(business=thebusiness,slug=slug)
    except ObjectDoesNotExist:
        return HttpResponse('Page Not Found')
    if thebusiness != businessline.business:
        #just raise an error
        raise ValueError
    first_letter = thebusiness.name[0].upper()
    if request.method == 'POST':
        body = request.body.decode('utf-8')
        body = json.loads(body)
        line = businessline.people_present.all()
        for eachuser in line:
            if eachuser.unique == body['remove']:
                if eachuser.present_line!=None:
                    eachuser.present_line = None
                    today = timezone.now()
                    t_spent  = today - eachuser.time
                    days_in_sec = t_spent.days * 86400
                    seconds = t_spent.seconds  
                    eachuser.total_seconds  = eachuser.total_seconds + days_in_sec + seconds
                    eachuser.save()
                    line_changed.send(sender=None,
                                      line_uniquefield=businessline.uniquefield)
        #just return something      
        return HttpResponse(1)
                
    else:
        today = timezone.now()
        time = today.time()
        open_or_closed='closed'
        all_days = {'mo':1,'tu':2,'we':3,'th':4,'fr':5,'sa':6,'su':7}
        inv_days = {1:'mo',2:'tu',3:'we',4:'th',5:'fr',6:'sa',7:'su'}
        days_open = thebusiness.days_open
        if days_open:
            days_open = ast.literal_eval(days_open)
        else:
            days_open = []
        tomorrow = False

        #business_local
        zone = pytz.timezone(thebusiness.timezone)
                            
        local_weekday = timezone.localdate(today,zone).isoweekday()
        local_date = timezone.localtime(today,zone)
        iso_days = []
        for all_ in all_days:
            if all_ in days_open:
                iso_days.append(all_days[all_])
        
        model_string = "thebusiness"       
        def generate(keyy,o=False):
            thebusiness
            open_exec_string = model_string+"."+keyy+"_o" 
            close_exec_string = model_string+"."+keyy+"_c"
            if o == 'o':
                return eval(open_exec_string)
            if o=='c':
                return eval(close_exec_string)
        
        weekday_open = False
        if local_weekday in iso_days:
            weekday_open = True
            for all_ in all_days:
                if all_days[all_] == local_weekday:
                    close_t = generate(all_,'c')
                    open_t = generate(all_,'o')
                    key = all_
                    break
            
                
            if (time >= open_t and time < close_t) or (close_t==open_t):
                open_or_closed ='open'
                
            elif '-' in str(close_t.hour - open_t.hour):
                time_lapse = (24 - open_t.hour) * 3600
                vx = datetime(today.year,
                                 today.month,
                                 today.day,
                                 open_t.hour,
                                 open_t.minute)
                vx = vx + timedelta(seconds=time_lapse)
                vy = datetime(today.year,
                                 today.month,
                                 today.day,
                                 close_t.hour,
                                 close_t.minute)
                vy = vy + timedelta(seconds=time_lapse)
                vz = today + timedelta(seconds=time_lapse)
                if (vz.time() >= vx.time() ) and vz.time() < vy.time():
                    open_or_closed ='open'
    
    
         
        
        if weekday_open and open_or_closed=='open':
            try:
                close_time = generate(key,'c')
                open_time = generate(key,'o')
                y = datetime(today.year,
                             today.month,
                             today.day,
                             close_time.hour,
                             close_time.minute)
                y = timezone.make_aware(y)
                closetimeee = timezone.localtime(y,zone).time()
                o_local_date = datetime(local_date.year,
                                             local_date.month,
                                             local_date.day,
                                             closetimeee.hour,
                                             closetimeee.minute)
                o_local_date = timezone.make_aware(o_local_date,zone)
                user_close_date = timezone.localtime(o_local_date,zone)
                closetime = '''{}'''.format(closetimeee.strftime("%I:%M %p"))
                opentime = ''
                
                user_today = timezone.localtime(today,zone)
                if user_today.isoweekday() != user_close_date.isoweekday():
                    tomorrow = True


            except ValueError:
                opentime  = ''
                closetime = ''
        else:
            # to confirm dates for user
            user_weekday = timezone.localdate(local_date,zone).isoweekday()
            user_date = timezone.localtime(local_date,zone)
            next_open = False
            
            
            
            for all_ in range(local_weekday,8):
                if inv_days[all_] in days_open:
                    next_open = all_
                    break
            
            if not next_open :#doesn"t open for rest of week
                for all_ in range(1,8):
                    if inv_days[all_] in days_open:
                        next_open = all_
                        break
                     
            

                
            #except day==next_open
            if next_open == local_weekday:
                close_time = generate(inv_days[local_weekday],'c')
                open_time = generate(inv_days[local_weekday],'o')
                x =datetime(today.year,
                             today.month,
                             today.day,
                             open_time.hour,
                             open_time.minute)
                x = timezone.make_aware(x)
                    
                y =datetime(today.year,
                                 today.month,
                                 today.day,
                                 close_time.hour,
                                 close_time.minute)
                y = timezone.make_aware(y)
                b_z = pytz.timezone(businessline.business.timezone)
                open_dtime = timezone.localtime(x,zone).time()
                close_dtime = timezone.localtime(y,zone).time()
                t_b = timezone.localtime(today,zone)
                #today_business
                if (t_b.time() >= close_dtime):
                    open_today = False
                else:
                    open_today = True
                if open_today == False:
                    if local_weekday==7:
                        rover = 1
                    else:
                        rover = local_weekday+1
                    for all_ in range(rover ,8):
                        if inv_days[all_] in days_open:
                            next_open = all_
                            break
                        else:
                            next_open = False
                    if not next_open :#doesn't open for rest of week
                        for all_ in range(1,8):
                            if inv_days[all_] in days_open:
                                next_open = all_
                                break
                    if next_open > local_weekday:
                        added_days = next_open - local_weekday
                    else:
                        added_days = (7 - local_weekday) + next_open
                        
                
                else:
                    added_days = 0
                    
            else:
                if next_open > local_weekday:
                    added_days = next_open - local_weekday
                else:
                    added_days = (7 - local_weekday) + next_open
            
        

                
            
            local_date_future = local_date + timedelta(days=added_days)
            try:
                close_time = generate(inv_days[local_date_future.isoweekday()],'c')
                open_time = generate(inv_days[local_date_future.isoweekday()],'o')
                new_day = today + timedelta(days=added_days)
                xx =    datetime(new_day.year,
                                 new_day.month,
                                 new_day.day,
                                 open_time.hour,
                                 open_time.minute)
                xx = timezone.make_aware(xx)
                opentimeee = timezone.localtime(xx,zone)
                opentimeee = timezone.localtime(opentimeee,zone).time()
                local_date_future = datetime(local_date_future.year,
                                             local_date_future.month,
                                             local_date_future.day,
                                             opentimeee.hour,
                                             opentimeee.minute)
                local_date_future = timezone.make_aware(local_date_future,zone)
                
                user_date_future = timezone.localtime(local_date_future,zone)
                rep = {1:'Monday',2:'Tuesday',3:'Wednesday',4:'Thursday',
                           5:'Friday',6:'Saturday',7:'Sunday'}
                wik_day = rep[user_date_future.isoweekday()]
                user_today = timezone.localtime(today,zone)
                if wik_day == rep[user_today.isoweekday()] and added_days==0:
                    wik_day = 'Today'
                elif wik_day == rep[user_today.isoweekday()] and added_days==7:
                    wik_day = 'next ' + wik_day
                opentime = '''{} at {}'''.format(wik_day,
                                                 user_date_future.strftime(
                                                     "%I:%M %p"))
                closetime = ''
            except (ValueError, AttributeError):
                opentime=''
                closetime=''
        
        
            
            
            
        
        line = businessline.people_present.all().order_by('time')
        number_of_people = len(line)
        form = RemoveForm()
        if not businessline:
            return HttpResponseRedirect (reverse('business:business_line'))
        line = line[:5]
            
        return render (request,
                           'business/homepage/detailview.html',
                           {'businessline': businessline,
                            'line':line,
                            'business':thebusiness,
                            'opentime':opentime,
                            'closetime':closetime,
                            'open_or_closed':open_or_closed,
                            'number_of_people':number_of_people,
                            'first_letter':first_letter,
                            'form':form})
            
       
    
    
@login_required
def ChangePasswordView(request):
    user = request.user
    try:
        business = user.business_signup
    except Exception:
        return HttpResponseRedirect(reverse('login'))
    if request.method == 'POST':
        password_form = ChangePasswordForm(request.user,request.POST)
        if password_form.is_valid():
            cd = password_form.cleaned_data
            user.set_password(cd['new_password'])
            user.save()
            login(request,user)
            messages.success(request,
                             'Your password was updated successfully!')
            return HttpResponseRedirect(reverse('business:business_homepage'))
        else:
            return render(request,'business/edit_registration/change_password.html',
                          {'password_form': password_form })
    else:
        password_form = ChangePasswordForm(request.user)
        return render(request,'business/edit_registration/change_password.html',
                          {'password_form': password_form })
        
        

        
     
@login_required
def DeleteBusinessLineView(request):
    if request.method == 'POST':
        form = DeleteBusinessLineForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = request.user
            normal_line = False
            try:
                user.business_signup
                line = Business_line.objects.get(uniquefield=cd['delete'])
                x = user.business_signup
                normal_line = True
                if line not in Business_line.objects.filter(business=x):
                    return HttpResponse('Something went wrong')
            except ObjectDoesNotExist:
                try:
                    user.user_signup
                    line = Special_line.objects.get(uniquefield=cd['delete'])
                    x = user.user_signup
                    if x != line.admin_user:
                        return HttpResponse('Something went wrong')
                except ObjectDoesNotExist:
                    return HttpResponse('Something went wrong')
            if normal_line:
                for all_ in line.people_present.all():
                    all_.present_line = None
                    all_.special_line = None
                    all_.save()
                line.delete()
                line_changed.send(sender=None,
                                      line_uniquefield=line.uniquefield)
                messages.success(request,'Line deleted successfully')
                return HttpResponseRedirect (reverse('business:business_homepage'))
            else:
                for all_ in line.all_present.all():
                    all_.present_line = None
                    all_.special_line = None
                    all_.save()
                line.delete()
                line_changed.send(sender=None,
                                      line_uniquefield=line.uniquefield)
                messages.success(request,'Line deleted successfully')
                return HttpResponseRedirect (reverse('users:user_homepage'))
            
    
        
    





    
    




            
        
