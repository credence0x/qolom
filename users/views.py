from django.shortcuts import render,get_object_or_404
from django.http import HttpResponseRedirect,HttpResponse,JsonResponse
from account.models import BusinessProfile
from business.models import BusinessQueue,Item,Order
from users.models import UserQueue
from django.contrib.auth.decorators import login_required
from .forms import SearchForm,CreateLineForm,EditLineForm,GetLocationForm,SearchByLocationForm,EditProfileForm,CheckKeyForm
from account.forms import ChangePasswordForm,DeleteBusinessLineForm
from django.contrib.auth import login
from django.db.models import Q
from django.urls import reverse
from django.contrib import messages
import json,math
from django.utils import timezone
from django.core.paginator import Paginator
from datetime import datetime,timedelta
import pytz,ast,requests
from business.forms import RemoveForm,JoinLineForm
from dateutil.parser import parse
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.sites.shortcuts import get_current_site
from random import choice
from django.core.cache import cache
from .signals import line_changed,notify_business
from django.db import IntegrityError
from standing.settings import PAYSTACK_SCRET_KEY,DEBUG
from django.views.decorators.clickjacking import xframe_options_exempt
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from account.tokens import account_activation_token_two
from django.core.mail import send_mail
from django.template import loader

def user_ajax(request,uniquefield,unique):
    #this function is called every few seconds to make sure user's position on the line is updated
    cache_ajax = cache.get(uniquefield,False)
    if cache_ajax:
        respond = cache_ajax.get(unique,False)
        # responds with user's position e.g 48 or 0 if user has left the line
        if respond:
            return HttpResponse(respond)
        else:
            cache.delete(uniquefield)
            return HttpResponse(0)
           
    else:
        key = uniquefield
        len_key = len(key)
        if len_key == 7:
            try:
                line = Business_line.objects.get(uniquefield=key).people_on_queue.all().order_by('time')
            except:
                return HttpResponse('pnf')#page not found
        elif len_key == 8:
            try:
                line = Special_line.objects.get(uniquefield=key).all_present.order_by('time')
            except:
                # page not found
                return HttpResponse('pnf')
        else:
            #page not found
            return HttpResponse('pnf')
        
        json_line = {}
        i=1
        for people in line:
            json_line[people.unique]=i
            i+=1
        cache.set(uniquefield,json_line,60)
        response = json_line.get(unique,False)
        
        if response:
            return HttpResponse(response)
        else:
            return HttpResponse(0)
    


def confirm_UserProfile_object(user):
    try:
        user = user.UserProfile
        return user
    except:
        return HttpResponseRedirect(reverse('login'))
def confirm_business_exists(business_key):
    try:
        business = BusinessProfile.objects.get(key=business_key)
        return business
    except:
        messages.error(request, 'Business does not exist')
        return HttpResponseRedirect(reverse('login'))

@login_required
def UserMenuView(request,key):
    user = request.user
    confirm_UserProfile_object(user)
    business = confirm_business_exists(key)
    # the first letter is collected so it can be used as an alternative 
    # to a display picture
    first_letter = business.name[0].upper()
    #items in the menu
    items = Items.objects.filter(business=business)# get all items associated with business
    return render (request,'users/payments/menu.html',
                                       {'items': items,
                                        'first_letter':first_letter,
                                        'business':business})
    

@login_required
def CheckOutView(request,key):
    user = request.user
    GET = []
    one = False
    # request.GET returns {item number : number ordered} for all items in the menu
    for all_ in request.GET:
        #get all the actual orders
        if request.GET.get(all_)!='0':
            GET.append(all_)
            one = True
    if not one:
        # no order..thus the only way they can be here is by tinkering with the url
        return HttpResponse('Stop playing with us')
    userr = confirm_UserProfile_object(user)
    business = confirm_business_exists(key)
    
    first_letter = business.name[0].upper()
    items = Items.objects.filter(id__in=GET)
    the_main_items = []
    total = 0
    def add_commas(figure):
        #add commas to figures before sending saving and sending it out
        figure = int(figure)
        return("{:,}".format(figure))
    
                    
                
    for each in items:
        #for all items in the cart
        units = request.GET.get(str(each.id)) # get the number of the each item ordered e.g 20 eggs 
        item_price = add_commas(each.price) 
        item_total = each.price * int(units)
        total += item_total
        the_main_items.append([each.name,item_price,units,str(each.id)])


    def split_float_and_add_commas(val):
        # takes in value like "300000.97"
        # so it splits to ["300000","97"]
        # then adds commas and rejoins ["30,000","97"] => "30,000.98"
        val = float(val)
        split_value = str(val).split('.')
        finish = add_commas(split_value[0])   +   '.'+ split_value[1]
        return finish

    
    #FEES
    def roundr(num, decimals=0):
        # round "num" to "decimal" decimal places 
        multiplier = 10 ** decimals
        return math.floor(num*multiplier + 0.5) / multiplier
    
    fees = (0.02 * total)
    fees = roundr(fees,2)
        
    if fees > 2500:
        fees = 2500.0
        # we collect not more than N2,500 in fees
    
    if total > 2500:
        fees = fees + 100
        # additional N100 if take out is more than 2,500
        if fees > 2500:
            fees = 2500.0
    
    real_total = split_float_and_add_commas(total)
    total = float(fees + total)
    amt = str(total).split('.')
    if len(amt[1])>1:
        tots = amt[0]+amt[1]
    else:
        tots = amt[0]+amt[1]+'0'
    
        
    
    fees = split_float_and_add_commas(fees)
        
  
        
    try:
        init_payment = requests.post(
                        'https://api.paystack.co/transaction/initialize',
                        headers={'Authorization': 'Bearer '+ PAYSTACK_SCRET_KEY,
                                 'Content-Type': 'application/json'},
                        json={'email':user.email,'amount':tots}
                        )
        
    except:
        total = split_float_and_add_commas(total)
        messages.error(request,'Something went wrong. Please reload page')
        return render (request,'users/payments/checkout.html',
                                       {'items': the_main_items,
                                        'total':total,
                                        'first_letter':first_letter,
                                        'business':business})
    if init_payment.json()['status']==False:
        total =split_float_and_add_commas(total)
        messages.error(request,'Something went wrong. Please reload page')
        return render (request,'users/payments/checkout.html',
                                       {'items': the_main_items,
                                        'total':total,
                                        'first_letter':first_letter,
                                        'business':business})
        
    link = init_payment.json()['data']['authorization_url']
    print(init_payment.json()['data'])
    
    ref = init_payment.json()['data']['reference']
    def get_rand_pin():
        num_string = ['1','2','3','4','5','6','7','8','9']#int makes 0 disappear thus not included
        value =""
        for num in range(6):
            value+=choice(num_string)
        return int(value)
    
    total = split_float_and_add_commas(total)
    new_order = Orders(reference=ref)
    new_order.total = real_total
    new_order.fees = fees
    new_order.user = userr
    new_order.status = 'Pending'
    new_order.items = str(the_main_items)
    new_order.business = business
    new_order.pin = get_rand_pin()
    time = timezone.now()
    new_order.created = time
    new_order.ready_time = time
    new_order.save()
    card_information = ast.literal_eval(user.UserProfile.card_information)
    return render (request,'users/payments/checkout.html',
                                       {'items': the_main_items,
                                        'total':total,
                                        'link':link,
                                        'fees':fees,
                                        'first_letter':first_letter,
                                        'business':business,
                                        'order':new_order,
                                        'card_information':card_information})


@login_required
def PayWithCardView(request,the_id,signature):
    user = confirm_UserProfile_object(request.user)
    
    the_order = Orders.objects.get(id=the_id,user=user)
    
    if the_order.is_active:
        #prevents multiple payment
        return HttpResponseRedirect(reverse('users:order',args=[the_id]))
    
    
    card = False
    all_cards = ast.literal_eval(user.card_information)
    for all_ in all_cards:
        if all_[3]==signature:
            card = all_[1]
            break
        
    if card:
        total = the_order.total
        r = ''
        for e in total:
            if e != ',':
                r+=e
        the_main = the_order.fees + float(r)
        r = str(the_main)
        tots = r.split('.')
        if len(tots[1])==1:
            tots = tots[0]+tots[1]+'0'
        else:
            tots = tots[0]+tots[1]
        print(tots)
        response = requests.post('https://api.paystack.co/transaction/charge_authorization',
                                 headers= {"Authorization": "Bearer " + PAYSTACK_SCRET_KEY,
                                           "Content-Type": "application/json"},
                                 json={ "authorization_code" : card,
                                        'email': request.user.email,
                                        'amount': tots,
                                        })
        
        
        if response.status_code == 200:
            the_data = response.json()['data']
            f_o_s = the_data['status']
            if f_o_s == 'success':
                for all_ in ast.literal_eval(the_order.items):
                    try:
                        change = Items.objects.get(id=all_[3])
                        new_units = change.units_available - int(all_[2])
                        if new_units < 0:
                            new_units = 0
                        change.units_available = new_units
                        change.save()
                    except ObjectDoesNotExist:
                        pass
                the_order.status ='PAID'
                time = timezone.now()
                the_order.is_active = True
                #the reference changes
                the_order.reference = the_data['reference']
                the_order.created = time
                the_order.order_status ='SENT'
                the_order.save()
                notify_business.send(sender=None,
                                          business=the_order.business)
                    
            else:
                the_order.status ='FAILED'
                the_order.is_active = True
                #the reference changes
                the_order.reference = the_data['reference']
                time = timezone.now()
                the_order.created = time
                the_order.order_status ='NOT SENT'
                the_order.save()
        else:
            # implement email myself thennnnnnnnnnnnn
            the_order.status ='FAILED'
            the_order.is_active = True
            time = timezone.now()
            the_order.created = time
            the_order.order_status ='NOT SENT'
            the_order.save()            

                            
    return HttpResponseRedirect(reverse('users:order',args=[the_order.id]))






@xframe_options_exempt
def VerifyPaymentScriptView(request):
    # payment verified
    reference = request.GET.get('reference')
    the_order = Orders.objects.get(reference=reference)
    the_order.is_active = True
    the_order.save()
    link = reverse('users:order',args=[the_order.id])
    return render (request,'users/payments/checkout_redirect_script.html',
                   {'link':link})

@xframe_options_exempt
@csrf_exempt
def webhook(request): #for paystack
    if request.method == 'POST':
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        if ip in ['129.205.124.243','52.31.139.75',
                  '52.49.173.169', '52.214.14.220']: #paystack ips for security
            body = request.body.decode('utf-8')
            body = json.loads(body)
            if body['event']=='charge.success':
                data = body['data']                
                try:
                    order = Orders.objects.get(reference=data['reference'])
                except:
                    #email myself
                    #development server
                    dev = True
                    order = Orders.objects.all()[0]
                    with transaction.atomic():
                        order = (
                              Orders.objects
                                .select_for_update()
                                  .get(id=2)
                                      )
                        
                        if order.status=='Pending' :
                            order.is_active = True
                            order.status ='PAID'
                            time = timezone.now()
                            order.created = time
                            order.order_status ='SENT'
                            order.save()
                            if not dev:
                                notify_business.send(sender=None,business=order.business)
        return HttpResponse(1)



@login_required
def SaveCardView(request):
    try:
        user = request.user.UserProfile
    except:
        return HttpResponseRedirect(reverse('login'))
    card_details = request.session.get('card_details',False)
    answer = request.GET.get('a',False)
    if card_details:
        if answer=='yes':
            del request.session['card_details']
            x = ast.literal_eval(user.card_information)
            info = [card_details['card_type'],
                    card_details['authorization_code'],
                    card_details['last_4'],
                    card_details['signature']
                    ]
            x.append(info)
            user.card_information = str(x)
            user.save()
            return HttpResponse('successful')
        else:
            del request.session['card_details']
    
    return HttpResponse('unsuccessful')


@login_required
def RemoveCardView(request):
    try:
        user = request.user.UserProfile
    except:
        return HttpResponseRedirect(reverse('login'))
    card = request.GET.get('sig',False)
    if card:
        info = ast.literal_eval(user.card_information)
        for all_ in info:
            if all_[3]==card:
                info.remove(all_)
                user.card_information=str(info)
                user.save()
                break
        return HttpResponse('successful')
    return HttpResponse('unsuccessful')




@login_required
def ManageCardView(request):
    try:
        user = request.user.UserProfile
    except:
        return HttpResponseRedirect(reverse('login'))
    card = ast.literal_eval(user.card_information)
    return render (request,'users/payments/manage_card.html',
                   {'card':card})
    

@login_required
def OrderView(request,identity):
    user = request.user
    ufo = confirm_UserProfile_object(user)
    the_order = Orders.objects.get(id=identity)
    zone = pytz.timezone(ufo.timezone)
    created_date = timezone.localtime(the_order.created,zone)
    
    days_past = False
    if (timezone.now() - the_order.created).days > 3:
        days_past = True
    if the_order.status=='Pending':
        response = requests.get('https://api.paystack.co/transaction/verify/' + the_order.reference,
                                headers={'Authorization': 'Bearer '+ PAYSTACK_SCRET_KEY})
        print(response.json())
        if response.status_code == 200:
            the_data = response.json()['data']
            f_o_s = the_data['status']
            
            if f_o_s == 'success':
                if the_data['channel']=='card':
                    one_exists = False
                    for baz in ast.literal_eval(ufo.card_information):
                        if baz[3]==the_data['authorization']['signature']:
                            one_exists = True
                            break
                    if not one_exists:
                        request.session['card_details']={
                            'card_type':the_data['authorization']['card_type'],
                            'last_4':the_data['authorization']['last4'],
                            'authorization_code':the_data['authorization']['authorization_code'],
                            'signature':the_data['authorization']['signature']
                            }
                for all_ in ast.literal_eval(the_order.items):
                    try:
                        change = Items.objects.get(id=all_[3])
                        new_units = change.units_available - int(all_[2])
                        if new_units < 0:
                            new_units = 0
                        change.units_available = new_units
                        change.save()
                    except ObjectDoesNotExist:
                        pass
                the_order.status ='PAID'
                time = timezone.now()
                the_order.created = time
                the_order.order_status ='SENT'
                the_order.save()
                notify_business.send(sender=None,
                                          business=the_order.business)
                
                
                
                
            else:
                the_order.status ='FAILED'
                the_order.is_active = True
                time = timezone.now()
                the_order.created = time
                the_order.order_status ='NOT SENT'
                the_order.save()
        else:
            
            #implement email myself
            the_order.status ='FAILED'
            the_order.is_active = True
            time = timezone.now()
            the_order.created = time
            the_order.order_status ='NOT SENT'
            the_order.save()

            
    if the_order.order_status=='READY':
        if not the_order.has_seen_notification:
            the_order.has_seen_notification = True
            the_order.save()
    items = ast.literal_eval(the_order.items)
    business = the_order.business
    total = the_order.total
    status = the_order.status
    order_status = the_order.order_status
    card_information = ast.literal_eval(ufo.card_information)
    return render(request,'users/payments/check_order.html',
                   {'items':items,
                    'order_status':order_status,
                    'business':business,
                    'status':status,
                    'order':the_order,
                    'created_date':created_date,
                    'total':total,
                    'days_past':days_past,
                    'card_details':request.session.get('card_details',False),
                    'card_information':card_information})

@login_required
def OrdersListView(request):
    user = request.user
    userr=confirm_UserProfile_object(user)
    changed = False
    orders = Orders.objects.filter(user=userr,is_active=True).order_by('-id')
    
    
    
                    
    for the_order in orders:
        if the_order.order_status=='READY':
            if not the_order.has_seen_notification:
                the_order.has_seen_notification = True
                the_order.save()
        
        if the_order.status=='Pending':
            response = requests.get('https://api.paystack.co/transaction/verify/' + the_order.reference,
                                    headers={'Authorization': 'Bearer '+ PAYSTACK_SCRET_KEY})
            
            if response.status_code!=200:
                response = requests.get('https://api.paystack.co/transaction/verify/' + the_order.reference,
                                    headers={'Authorization': 'Bearer '
                                             + 'sk_test_dba3ece03b5a28cc32f000e6eb82ff58e5d690e7'})
            print(response.json()['data'])
            if response.status_code == 200:
                the_data = response.json()['data']
                f_o_s = the_data['status']
                if f_o_s == 'success':
                    
                    if the_data['channel']=='card':
                        one_exists = False
                        for baz in ast.literal_eval(userr.card_information):
                            if baz[3]==the_data['authorization']['signature']:
                                one_exists = True
                                break
                        if not one_exists:
                            request.session['card_details']={
                                'card_type':the_data['authorization']['card_type'],
                                'last_4':the_data['authorization']['last4'],
                                'authorization_code':the_data['authorization']['authorization_code'],
                                'signature':the_data['authorization']['signature']
                                }
                    
                    for all_ in ast.literal_eval(the_order.items):
                        try:
                            change = Items.objects.get(id=all_[3])
                            new_units = change.units_available - int(all_[2])
                            if new_units < 0:
                                new_units = 0
                            change.units_available = new_units
                            change.save()
                        except ObjectDoesNotExist:
                            pass
                    the_order.status ='PAID'
                    time = timezone.now()
                    the_order.created = time
                    the_order.order_status ='SENT'
                    the_order.save()
                    notify_business.send(sender=None,
                                                  business=the_order.business)
                    
                        
                        
                        
                elif f_o_s=='abandoned':
                    the_order.delete()
                    changed = True
                    
                else:
                    the_order.status ='FAILED'
                    the_order.is_active = True
                    time = timezone.now()
                    the_order.created = time
                    the_order.order_status ='NOT SENT'
                    the_order.save()
            else:
                pass
                #email myself
    if changed:
        orders = Orders.objects.filter(user=userr,is_active=True).order_by('-id')
    paginator = Paginator(orders, 40)
    page_number = request.GET.get('page')
    orders = paginator.get_page(page_number)
    return render(request,'users/payments/list_orders.html',
                   {'orders':orders})
@login_required
def CheckReadyAPIView(request):
    user = request.user
    try:
        userr = user.UserProfile
    except:
        return HttpResponseRedirect(reverse('login'))
    params = request.GET.get('i',False)
    if params:
        order = Orders.objects.get(user=userr,id=params)
        if order.order_status == 'READY':
            return HttpResponse('yes')
        else:
            return HttpResponse('no')
    
    
    

@login_required
def CheckKeyView(request):
    user = request.user
    try:
        ufo = user.UserProfile
    except:
        return HttpResponseRedirect(reverse('login'))
    if request.method=='POST':
        form = CheckKeyForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data.get('key')
            if len(cd) < 7 or len(cd)> 8:
                form.add_error('key','No match found' )
                return render (request,'users/homepage/findkey.html',
                                       {'key_form': form})
            business = False
            if len(cd)==7:
                business = True
            if business:
                try:
                    business = BusinessProfile.objects.get(key=cd)
                    if user.UserProfile.iso_code != business.iso_code:
                        form.add_error('key',
                                       ''' You can only join queues located in your country. Edit your profile if you are not in {}.'''
                                       .format(ufo.country))
                        return render (request,
                                       'users/homepage/findkey.html',
                                       {'key_form': form})
                    return HttpResponseRedirect(reverse('users:user_detailview',
                                                        args=[cd,business.slug]))
                except ObjectDoesNotExist:
                    form.add_error('key','No match found' )
                    return render (request,
                                       'users/homepage/findkey.html',
                                       {'key_form': form})
            else:
                try:
                    line = Special_line.objects.get(uniquefield=cd)
                    return HttpResponseRedirect(reverse('users:line',args=[cd]))
                except ObjectDoesNotExist:
                    form.add_error('key','No match found' )
                    return render (request,
                                       'users/homepage/findkey.html',
                                       {'key_form': form})
        else:
            return render (request,'users/homepage/findkey.html',
                                {'key_form': form})
    else:
        form = CheckKeyForm()
        return render (request,'users/homepage/findkey.html',
                                {'key_form': form})
        
                    
                    
                
        
    


        






    
@login_required
def user_line(request,unumber):
    unumber = unumber
    user = request.user
    normal_line = False
    person = confirm_UserProfile_object(user)
    if len(unumber)==7:
        try:
            businessline = Business_line.objects.get(uniquefield=unumber)
            business = businessline.business
            legal = True
            age = person.age
            if business.min_age!=0:
                then = datetime(age.year,age.month,age.day,tzinfo=pytz.utc)
                now = timezone.now()
                lapse = now-then
                if lapse.days/365 < business.min_age:
                    legal = False
            if not legal:
                return HttpResponseRedirect(reverse('users:user_detailview',
                                                    args=[business.key,
                                                          business.slug]))
            first_letter = business.name[0].upper()
            b_z = pytz.timezone(business.timezone)
            normal_line = True
        except ObjectDoesNotExist:    
            return HttpResponse('Page Not Found')
    else:
        try:
            businessline = Special_line.objects.get(uniquefield=unumber)
            business = businessline.admin_user
            first_letter = business.first_name[0].upper()#remove later
            b_z = pytz.timezone(businessline.admin_user.timezone)
        except ObjectDoesNotExist:
            return HttpResponse('Page Not Found')

    
    
    if normal_line == True:
        line = businessline.people_on_queue.all().order_by('time')
        len_line = line.count()
    else:
        line = businessline.all_present.all().order_by('time')
        len_line = line.count()
    today = timezone.now()
    time = today.time()
    open_or_closed='closed'
    all_days = {'mo':1,'tu':2,'we':3,'th':4,'fr':5,'sa':6,'su':7}
    inv_days = {1:'mo',2:'tu',3:'we',4:'th',5:'fr',6:'sa',7:'su'}
    if normal_line:
        days_open = business.days_open
        if days_open:
            days_open = ast.literal_eval(days_open)
        else:
            days_open=[]
    else:
        days_open = businessline.days_open
    tomorrow = False

    #business_local
    zone = pytz.timezone(person.timezone)
                        
    local_weekday = timezone.localdate(today,b_z).isoweekday()
    local_date = timezone.localtime(today,b_z)
    iso_days = []
    for all_ in all_days:
        if all_ in days_open:
            iso_days.append(all_days[all_])
    if normal_line:
        model_string = "business"
    else:
        model_string= "businessline"
    
    def generate(keyy,o=False):
        businessline or business #makes object available for eval("business or businessline_**_*")# don't ask me how
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
            # vx,vy are relevant
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
            closetime_1 = timezone.localtime(y,b_z)
            closetimeee = timezone.localtime(closetime_1,zone).time()
            o_local_date = datetime(local_date.year,
                                         local_date.month,
                                         local_date.day,
                                         closetime_1.hour,
                                         closetime_1.minute)
            o_local_date = timezone.make_aware(o_local_date,b_z)
                
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
        zone = pytz.timezone(person.timezone)
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
            open_dtime = timezone.localtime(x,b_z).time()
            close_dtime = timezone.localtime(y,b_z).time()
            t_b = timezone.localtime(today,b_z)
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
            opentime_1 = timezone.localtime(xx,b_z)
            opentimeee = timezone.localtime(opentime_1,zone).time()
            local_date_future = datetime(local_date_future.year,
                                         local_date_future.month,
                                         local_date_future.day,
                                         opentime_1.hour,
                                         opentime_1.minute)
            local_date_future = timezone.make_aware(local_date_future,b_z)
            
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
        except (ValueError,AttributeError):
            opentime=''
            closetime=''
           
            
    
    if request.method == 'POST':
        if normal_line:
            join_line_form = JoinLineForm(request.POST)
            if join_line_form.is_valid():
                cd = join_line_form.cleaned_data.get('join')
                if person.first_name == cd:
                    if open_or_closed=='open':
                        if person.present_line != None or person.special_line != None:
                            t_spent  = today - person.time
                            days_in_sec = t_spent.days * 86400
                            seconds = t_spent.seconds  
                            person.total_seconds  = person.total_seconds + days_in_sec + seconds
                        if person.present_line != businessline:
                            person.present_line = businessline
                            person.special_line = None
                            person.time = today
                            person.save()
                            line_changed.send(sender=None,
                                              line_uniquefield=unumber
                                              )
                        else:
                            # so the person doesnt end up in back of line again
                            pass  
                        inline = True
                        join_line_form = JoinLineForm()
                        number = 1
                        for people in line:
                            if person == people:
                                break
                            number += 1
                        
                        k = business.get_absolute_url()
                        l = business.user.first_name
                        new_session_data ={'url':k , 'name':l}
                        sess = request.session.get('recent',None)
                        
                        if sess:
                            newv = request.session['recent']
                            if new_session_data in newv:
                                for element in sess:
                                    if new_session_data == element:
                                        newv.remove(new_session_data)
                                        newv.insert(0,new_session_data)
                                        request.session.modified = True
                                        break
                            else:     
                                newv.insert(0,new_session_data)
                                if len(newv)> 5:
                                    newv.pop(-1)
                                request.session.modified = True
                        else:
                            request.session['recent'] = []
                            j = request.session['recent']
                            j.append(new_session_data)
                            request.session.modified = True
                        ten = range(1,11)
                        
                        return render (request,
                                       'users/homepage/linedetailview.html',
                                       {'businessline': businessline,
                                        'person':person,
                                        'inline': inline,
                                        'len_line':len_line,
                                        'ten':ten,
                                        'business':business,
                                        'weekday_open':weekday_open,
                                        'number':number,
                                        'open_or_closed':open_or_closed,
                                        'opentime':opentime,
                                        'closetime':closetime,
                                        'first_letter':first_letter,
                                        'tomorrow':tomorrow,
                            
                                        'join_line_form':join_line_form})
                        
                    else:
                        return HttpResponseRedirect(
                            reverse('users:line',args=[unumber]))
                elif person.ticket == cd:
                        # used ticket for when person wants to exit
                    if person.present_line != None:
                        #businessline is nt needed here
                        person.present_line = None
                        t_spent  = today - person.time
                        days_in_sec = t_spent.days * 86400
                        seconds = t_spent.seconds  
                        person.total_seconds  = person.total_seconds + days_in_sec + seconds
                        person.save()
                        len_line = len_line - 1 #you
                        
                        line_changed.send(sender=None,
                                          line_uniquefield=unumber)
                        inline = False    
                        join_line_form = JoinLineForm()
                    
                        k = business.get_absolute_url()
                        l = business.name
                        new_session_data ={'url':k , 'name':l}
                        sess = request.session.get('recent',None)
                        if sess:
                            newv = request.session['recent']
                            if new_session_data in newv:
                                for element in sess:
                                    if new_session_data == element:
                                        newv.remove(new_session_data)
                                        newv.insert(0,new_session_data)
                                        request.session.modified = True
                                        break
                            else:     
                                newv.insert(0,new_session_data)
                                if len(newv)> 5:
                                    newv.pop(-1)
                                request.session.modified = True
                        else:
                            request.session['recent'] = []
                            j = request.session['recent']
                            j.append(new_session_data)
                            request.session.modified = True                    
                        return render (request,
                                   'users/homepage/linedetailview.html',
                                       {'businessline': businessline,
                                        'person':person,
                                        'inline': inline,
                                        'business':business,
                                        'open_or_closed':open_or_closed,
                                        'len_line':len_line,
                                        'opentime':opentime,
                                        'closetime':closetime,
                                        'weekday_open':weekday_open,
                                        'first_letter':first_letter,
                                        'tomorrow':tomorrow,
                                        'join_line_form':join_line_form})
                    else:
                        inline=False
                        join_line_form = JoinLineForm()    
                        return render (request,
                                       'users/homepage/linedetailview.html',
                                       {'businessline': businessline,
                                        'person':person,
                                        'inline': inline,
                                        'weekday_open':weekday_open,
                                        'open_or_closed':open_or_closed,
                                        'len_line':len_line,
                                        'opentime':opentime,
                                        'closetime':closetime,
                                        'business':business,
                                        'tomorrow':tomorrow,
                                        'first_letter':first_letter,
                                        'join_line_form':join_line_form})
                        

        else:
            #special_line
            join_line_form = JoinLineForm(request.POST)
            if join_line_form.is_valid():
                cd = join_line_form.cleaned_data.get('join')
                if person.first_name == cd:
                    if open_or_closed=='open':
                        if person.special_line != None or person.present_line!=None:
                            t_spent  = today - person.time
                            days_in_sec = t_spent.days * 86400
                            seconds = t_spent.seconds  
                            person.total_seconds  = person.total_seconds + days_in_sec + seconds

    


                            
                        if person.special_line != businessline:
                            person.special_line = businessline
                            
                            if person.present_line:
                                # to add to recently visited
                                k = person.present_line.business.get_absolute_url()
                                l = person.present_line.business.name
                                new_session_data ={'url':k , 'name':l}
                                sess = request.session.get('recent',None)
                                if sess:
                                    newv = request.session['recent']
                                    if new_session_data in newv:
                                        for element in sess:
                                            if new_session_data == element:
                                                newv.remove(new_session_data)
                                                newv.insert(0,new_session_data)
                                                request.session.modified = True
                                                break
                                    else:     
                                        newv.insert(0,new_session_data)
                                        if len(newv)> 5:
                                            newv.pop(-1)
                                        request.session.modified = True
                                else:
                                    request.session['recent'] = []
                                    j = request.session['recent']
                                    j.append(new_session_data)
                                    request.session.modified = True
                                
                            person.present_line = None
                            person.time = today
                            person.save()
                            line_changed.send(sender=None,
                                              line_uniquefield=unumber)
                        else:
                            # so the person doesnt end up in back of line again
                            pass
                        inline = True
                        join_line_form = JoinLineForm()
                        number = 1
                        for people in line:
                            if person == people:
                                break
                            number += 1
                        
                        ten = range(1,11)    
                        return render (request,
                                       'users/special/user/linedetailview.html',
                                       {'businessline': businessline,
                                        'person':person,
                                        'inline': inline,
                                        'len_line':len_line,
                                        'ten':ten,
                                        'business':business,
                                        'weekday_open':weekday_open,
                                        'number':number,
                                        'open_or_closed':open_or_closed,
                                        'opentime':opentime,
                                        'closetime':closetime,
                                        'first_letter':first_letter,
                                        'tomorrow':tomorrow,
                            
                                        'join_line_form':join_line_form})
                    else:
                        return HttpResponseRedirect(
                            reverse('users:line',args=[unumber]))
                elif person.ticket == cd:
                        # used ticket for when person wants to exit
                    if person.special_line!=None:
                        person.special_line = None
                        t_spent  = today - person.time
                        days_in_sec = t_spent.days * 86400
                        seconds = t_spent.seconds  
                        person.total_seconds  = person.total_seconds + days_in_sec + seconds
                        person.save()
                        len_line = len_line -1 #you
                        line_changed.send(sender=None,
                                          line_uniquefield=unumber)
                        inline = False    
                        join_line_form = JoinLineForm()  
                        return render (request,
                                   'users/special/user/linedetailview.html',
                                       {'businessline': businessline,
                                        'person':person,
                                        'inline': inline,
                                        'open_or_closed':open_or_closed,
                                        'len_line':len_line,
                                        'opentime':opentime,
                                        'closetime':closetime,
                                        'weekday_open':weekday_open,
                                        'business':business,
                                        'first_letter':first_letter,
                                        'tomorrow':tomorrow,
                                        'join_line_form':join_line_form})
                    else:
                        inline=False
                        join_line_form = JoinLineForm()    
                        return render (request,
                                       'users/special/user/linedetailview.html',
                                       {'businessline': businessline,
                                        'person':person,
                                        'inline': inline,
                                        'weekday_open':weekday_open,
                                        'open_or_closed':open_or_closed,
                                        'len_line':len_line,
                                        'business':business,
                                        'opentime':opentime,
                                        'closetime':closetime,
                                        'first_letter':first_letter,
                                        'tomorrow':tomorrow,
                                        'join_line_form':join_line_form})






                        
    else:
        #request GET
        join_line_form = JoinLineForm()
        number = 0#significant check template
        if normal_line:
            if person.present_line == businessline:
                inline = True
            else:
                inline = False
            if person in line:
                number = 1
                for people in line:
                    if people == person:
                        break
                    number +=1

            ten = range(1,11)    
            return render (request,
                          'users/homepage/linedetailview.html',
                        {'businessline': businessline,
                            'person':person,
                            'inline':inline,
                            'len_line':len_line,
                            'ten':ten,
                            'weekday_open':weekday_open,
                            'opentime':opentime,
                            'closetime':closetime,
                            'business':business,
                            'tomorrow':tomorrow,
                            'open_or_closed':open_or_closed,
                            'number':number,
                            'first_letter':first_letter,
                            'join_line_form':join_line_form})
            


        else:
            if person.special_line == businessline:
                inline = True
            else:
                inline = False
            if person in line:
                number = 1
                for people in line:
                    if people == person:
                        break
                    number +=1

            ten = range(1,11)    
            return render (request,
                           'users/special/user/linedetailview.html',
                           {'businessline': businessline,
                            'person':person,
                            'inline':inline,
                            'len_line':len_line,
                            'ten':ten,
                            'weekday_open':weekday_open,
                            'opentime':opentime,
                            'closetime':closetime,
                            'business':business,
                            'tomorrow':tomorrow,
                            'open_or_closed':open_or_closed,
                            'number':number,
                            'first_letter':first_letter,
                            'join_line_form':join_line_form})
                

@login_required
def UserHomePageView(request):
    user = request.user
    try:
        person = user.UserProfile
    except:
        return HttpResponseRedirect(reverse('login'))
    
    try:
        xx = person.admin_special_line
        date = xx.created
        today = timezone.now()
        if today > date + timedelta(days=10):
            any_u = xx.all_present.all()
            if any_u:
                pass
            else:
                xx.delete()
    except ObjectDoesNotExist:
        pass
    line = False
    normal_line = person.present_line
    special_line = person.special_line
    if normal_line:
        line = normal_line
        people = line.people_on_queue.all().order_by('time')
    elif special_line:
        line = special_line        
        people = line.all_present.all().order_by('time')
    if request.method == 'GET':
        cd = request.GET.get('search',False)
        if cd:
            if '/' in cd:
                wix = ''
                for bib in cd:
                    if bib == '/':
                        wix += '%2F'
                    else:
                        wix += bib
                cd = wix
                    
            return HttpResponseRedirect(reverse('users:search')+'?search='+cd)
                                        
            
            
                    
        #other normal function
        #what happens when location changes.....watchlocation javascript and distance
        form = SearchForm()
        all_businesses = BusinessProfile.objects.all()
        ts = person.total_seconds
        td = timedelta(seconds=ts)
        days = td.days
        h_m_s = str(timedelta(seconds=td.seconds))
        h_m_s = h_m_s.split(':')
        hours = h_m_s[0]
        minutes = h_m_s[1]
        seconds = h_m_s[2]
        total_time = "{} hours, {} minutes, {} seconds".format(hours,
                                                               minutes,
                                                               seconds)
        if days > 1:
            total_time = "{} days, {} hours, {} minutes, {} seconds".format(days,hours,
                                                               minutes,
                                                               seconds)
        elif days == 1:
            total_time = "{} day, {} hours, {} minutes, {} seconds".format(days,hours,
                                                               minutes,
                                                               seconds)
                
        recent = request.session.get('recent',False)
        get_loc = GetLocationForm()
        homepage = True
        if line:
            number = 0
            for you in people:
                number += 1 
                if person == you:
                    break
            
            return render(request,'users/homepage/homepage.html',
                          {'form':form,
                           'number':number,
                           'line':line,
                           'get_loc':get_loc,
                           'homepage':homepage,
                           'recent':recent,
                           'total_time':total_time,
                           'person':person})
        return render(request,'users/homepage/homepage.html',
                          {'form':form,
                           'homepage':homepage,
                           'recent':recent,
                           'get_loc':get_loc,
                           'total_time':total_time,
                           'person':person})


@login_required
def GetLocationView(request):
    user = request.user
    try:
        person = user.UserProfile
    except:
        return HttpResponse('Failed')
    if request.method == 'GET':
        cd = request.GET
        if cd:
            loc = {'country_code':cd.get('country_code'),
                 'state':cd.get('statin'),
                 'city':cd.get('cty'),
                 'locality':cd.get('locaty')}
            request.session['location'] = loc
            request.session['loc_time']= str(timezone.now())
            
    return HttpResponse('done')
                                        
            
            
                    
        
       
        





    

@login_required    
def SearchPageView(request):
    ccc= timezone.now()
    try:
        some_variable = request.user.UserProfile
    except:
        return HttpResponseRedirect(reverse('login'))
    business_name = request.GET.get('search',False)
    s_b_l = request.GET.get('s_b_l',False)
    get_loc = GetLocationForm()
    
    if request.method == 'GET':
        if s_b_l:
            data = {'search':business_name}
            form = SearchForm(initial=data)
            loc_form = SearchByLocationForm({'s_b_l':s_b_l})
            results = BusinessProfile.objects.filter(Q(name__icontains=business_name),
                                                     Q(address__icontains=s_b_l)|Q(state__icontains=s_b_l))
            

            new_results =[]
            others =[]
            result_list = list(results[:5000])
            count = 0
            cunt = True
            for all_ in result_list:
                if business_name.lower() == all_.name[:len(business_name)].lower():
                    new_results.append(all_)
                else:
                    others.append(all_)
            for all_ in others:
                new_results.append(all_)
            results = new_results
            paginator = Paginator(results, 20)
            page_number = request.GET.get('page')
            results = paginator.get_page(page_number)
            
            return render(request,'users/homepage/searchpage.html',
                              {'results':results,
                               'form':form,
                               'get_loc':get_loc,
                               'loc_form':loc_form,
                               'result_for_business':business_name,
                               'result_for_loc':s_b_l})
        
        #else
        person = request.user.UserProfile
        data = {'search':business_name}
        form = SearchForm(initial=data)
        loc_search = request.session.get('loc_search')
        close_to_you = None
        has_location = request.session.get('location',False)
        if has_location == '#':
            del request.session['location']
            has_location = False
        
        
        if has_location:
            #remove the next line, there can be location errors
            country_code = request.session['location']['country_code']
            state        = request.session['location']['state'].lower()
            city         = request.session['location']['city'].lower()
            locality     = request.session['location']['locality'].lower()
            loc_form = SearchByLocationForm()
            
            results = BusinessProfile.objects.filter(Q(iso_code=person.iso_code),
                                                     Q(name__icontains=business_name)
                                                     ).order_by('state','name')
            
            if not results.exists():
                results=False
                return render(request,'users/homepage/searchpage.html',
                                           {'results':results,
                                           'form':form,
                                            'get_loc':get_loc,
                                            'result_for_business':business_name,
                                            'result_for_loc':s_b_l})
            queryset = results.filter(state__iexact=state)
            
            
            if queryset.exists():
                if city != 'undefined':
                    h_o_s=False
                    if '-' in city:
                        h_o_s = '-'
                    elif ' ' in city:
                        h_o_s = ' '
                    if h_o_s:
                        split_city = city.split('-')
                        close_to_you=queryset.filter(address__icontains=split_city[0]
                                                     )[:10]
                    else:
                        close_to_you=queryset.filter(address__icontains=city
                                                     )[:10]
                        
                elif locality != 'undefined':
                    h_o_s=False
                    if '-' in locality:
                        h_o_s = '-'
                    elif ' ' in locality:
                        h_o_s = ' '
                    if h_o_s:
                        split_locality = locality.split('-')
                        close_to_you=queryset.filter(address__icontains=split_locality[0]
                                                     )[:10]
                          
                    else:
                        close_to_you = queryset.filter(address__icontains=locality)[:20]
                
                new_results =[]
                others=[]
                no_match =[]
                state_results =[]
                l_b_n = len(business_name)
                
                result_list = list(results[:5000])
                
                
                
                for all_ in result_list:
                    if all_.state.lower()==state:
                        state_results.append(all_)
                    else:
                        others.append(all_)
                        
                 
                for all_ in state_results:
                    if business_name.lower()==all_.name[:l_b_n].lower():
                        new_results.append(all_)
                    else:
                        no_match.append(all_)
                
                for all_ in others:
                    if business_name.lower() == all_.name[:l_b_n].lower():
                        new_results.append(all_)
                    else:
                        no_match.append(all_)
                for all_ in no_match:
                    new_results.append(all_)
                
                
                
                results = new_results
                paginator = Paginator(results, 20)
                page_number = request.GET.get('page',1)
                results = paginator.get_page(page_number)
                return render(request,'users/homepage/searchpage.html',
                                           {'results':results,
                                           'form':form,
                                            'close_to_you':close_to_you,
                                           'loc_form':loc_form,
                                            'get_loc':get_loc,
                                            'result_for_business':business_name,
                                            'result_for_loc':s_b_l})
            else:
                possible_words=[' district',' province',' county',' division',
                            ' department',' parish',' state','provincia de ',
                            ' municipality',' governate',' atoll',' city',' pradesh',
                            ' quarter',' provincia', ' region']
                for word in possible_words:
                    if word in state:
                        state = state.replace(word,'')
                        break
                queryset=results.filter(state__icontains=state)
                if queryset.exists():
                    if city != 'undefined':
                        h_o_s=False
                        if '-' in city:
                            h_o_s = '-'
                        elif ' ' in city:
                            h_o_s = ' '
                        if h_o_s:
                            split_city = city.split('-')
                            close_to_you=queryset.filter(address__icontains=split_city[0]
                                                         )[:10]
                        else:
                            close_to_you=queryset.filter(address__icontains=city
                                                         )[:10]
                        
                    elif locality != 'undefined':
                        h_o_s=False
                        if '-' in locality:
                            h_o_s = '-'
                        elif ' ' in locality:
                            h_o_s = ' '
                        if h_o_s:
                            split_locality = locality.split('-')
                            close_to_you=queryset.filter(address__icontains=split_locality[0]
                                                         )[:10]
                          
                        else:
                            close_to_you = queryset.filter(address__icontains=locality)[:10]
                    new_results =[]
                    others=[]
                    no_match =[]
                    state_results =[]
                    l_b_n = len(business_name)
                    result_list = list(results[:5000])
                
                    for all_ in result_list:
                        if all_.state.lower()==state:
                            state_results.append(all_)
                        else:
                            others.append(all_)    
                    for all_ in state_results:
                        if business_name.lower()==all_.name[:l_b_n].lower():
                            new_results.append(all_)
                        else:
                            no_match.append(all_)
                
                    for all_ in others:
                        if business_name.lower() == all_.name[:l_b_n].lower():
                            new_results.append(all_)
                        else:
                            no_match.append(all_)
                    for all_ in no_match:
                        new_results.append(all_)
                    results = new_results
                    paginator = Paginator(results, 20)
                    page_number = request.GET.get('page')
                    results = paginator.get_page(page_number)
                    return render(request,'users/homepage/searchpage.html',
                                               {'results':results,
                                               'form':form,
                                                'get_loc':get_loc,
                                                'close_to_you':close_to_you,
                                               'loc_form':loc_form,
                                                'result_for_business':business_name,
                                                'result_for_loc':s_b_l})
                else:#no state
                    new_results =[]
                    others =[]
                    result_list = list(results[:5000])
                    count = 0
                    cunt = True
                    for all_ in result_list:
                        if business_name.lower() == all_.name[:len(business_name)].lower():
                            new_results.append(all_)
                        else:
                            others.append(all_)
                    for all_ in others:
                        new_results.append(all_)
                    results = new_results
                    paginator = Paginator(results, 20)
                    page_number = request.GET.get('page')
                    results = paginator.get_page(page_number)
                    return render(request,'users/homepage/searchpage.html',
                                               {'results':results,
                                               'form':form,
                                                'get_loc':get_loc,
                                               'loc_form':loc_form,
                                               'result_for_business':business_name,
                                               'result_for_loc':s_b_l})
                    

                




            
        else:
            data = {'search':business_name}
            loc_form = SearchByLocationForm(initial=data)
            results = BusinessProfile.objects.filter(Q(iso_code=person.iso_code),
                                                     Q(user__first_name__icontains=business_name)
                                                     ).order_by('state','user__first_name')
            if not results.exists():
                # dont show form to save space
                return render(request,'users/homepage/searchpage.html',
                                       {'results':results,
                                       'form':form,
                                        'get_loc':get_loc,
                                       'result_for_business':business_name,
                                       'result_for_loc':s_b_l})
            new_results =[]
            others =[]
            result_list = list(results[:5000])     
            for all_ in result_list:
                if business_name.lower() == all_.name[:len(business_name)].lower():
                    new_results.append(all_)
                else:
                    others.append(all_)
            for all_ in others:
                new_results.append(all_)
            results = new_results
            paginator = Paginator(results, 20)
            page_number = request.GET.get('page')
            results = paginator.get_page(page_number)
            return render(request,'users/homepage/searchpage.html',
                                  {'results':results,
                                   'form':form,
                                   'get_loc':get_loc,
                                   'loc_form':loc_form,
                                   'result_for_business':business_name,
                               'result_for_loc':s_b_l})
    

    
@login_required
def UserDetailView(request,key,slug):
    try:
        person = request.user.UserProfile
    except:
        return HttpResponseRedirect(reverse('login'))
    key = key
    slug = slug
    #use get object or 404
    business = BusinessProfile.objects.get(key=key)
    age = person.age
    legal = True
    if business.min_age!=0:
        then = datetime(age.year,age.month,age.day,tzinfo=pytz.utc)
        now = timezone.now()
        asaba = now-then
        if asaba.days/365 < business.min_age:
            print(asaba.days/365)
            legal = False
    parameter = request.GET.get('p',None)
    first_letter = business.name[0].upper()
    if parameter:
        if parameter == 'fav':
            person.favourites.add(business)
            return HttpResponse('a')
        elif parameter == 'rfav':
            person.favourites.remove(business)
            return HttpResponse('r')
    current_site = get_current_site(request)
    line = Business_line.objects.filter(business=business).order_by('name')


    ####################### ABOUT TIME ##############################
            
    b_z = pytz.timezone(business.timezone)
    today = timezone.now()
    time = today.time()
    open_or_closed='closed'
    all_days = {'mo':1,'tu':2,'we':3,'th':4,'fr':5,'sa':6,'su':7}
    inv_days = {1:'mo',2:'tu',3:'we',4:'th',5:'fr',6:'sa',7:'su'}
    days_open = business.days_open
    if days_open:
        days_open = ast.literal_eval(days_open)
    else:
        days_open=[]
    tomorrow = False

    #business_local
    zone = pytz.timezone(person.timezone)   
    local_weekday = timezone.localdate(today,b_z).isoweekday()
    local_date = timezone.localtime(today,b_z)
    iso_days = []
    for all_ in all_days:
        if all_ in days_open:
            iso_days.append(all_days[all_])
    
    model_string = "business"
    def generate(keyy,o=False):
        business #makes object available for eval("business or businessline_**_*")# don't ask me how
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
            # vx,vy are relevant
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


                

                
    return render(request,'users/homepage/detailview.html',{'business':business,
                                                            'domain': current_site.domain,
                                                            'line':line,
                                                            'closetime':closetime,
                                                            'opentime':opentime,
                                                            'open_or_closed':open_or_closed,
                                                            'first_letter':first_letter,
                                                            'person':person,
                                                            'legal':legal})


    
@login_required
def EditView(request):
    user = request.user
    try:
        person = user.UserProfile
    except:
        return HttpResponseRedirect(reverse('login'))
    tz = pytz.timezone(person.timezone).utcoffset
    data = {'first_name':user.first_name,
                'last_name':user.last_name,
            'country':person.country,
            'iso_code':person.iso_code,
            'timezone':person.timezone}
    if request.method == 'POST':
        edit_form = EditProfileForm(request.user,request.POST)
        if edit_form.is_valid():
            cd = edit_form.cleaned_data
            # modify user object
            user.first_name = cd['first_name']
            user.last_name = cd['last_name']
            user.save()
          # modify related UserProfile
            person.country = cd['country']
            person.first_name = cd['first_name']
            person.last_name = cd['last_name']
            person.iso_code = cd['iso_code']
            person.timezone = cd['timezone']
            person.save()
            messages.success(request,
                             'Your profile was updated successfully!')
            return HttpResponseRedirect(reverse('users:user_homepage'))
        else:
            return render(request,'users/edit_registration/editview.html',
                      {'edit_form':edit_form})
    else:
        edit_form = EditProfileForm(request.user,initial=data)
        return render(request,'users/edit_registration/editview.html',
                      {'edit_form':edit_form})

@login_required
def ChangePasswordView(request):
    user = request.user
    try:
        person = user.UserProfile
    except:
        return HttpResponseRedirect(reverse('login'))

    if request.method == 'POST':
        password_form = ChangePasswordForm(request.user,request.POST)
        if password_form.is_valid():
            cd = password_form.cleaned_data
            user.set_password(cd['new_password'])
            user.save()
            login(request,user)
            messages.success(request, 'Your password was updated successfully!') 
            return HttpResponseRedirect(reverse('users:user_homepage'))
        else:
            return render(request,'users/edit_registration/change_password.html',
                          {'password_form': password_form })
    else:
        password_form = ChangePasswordForm(request.user)
        return render(request,'users/edit_registration/change_password.html',
                          {'password_form': password_form })

@login_required
def FavouritesView(request):
    try:
        some_variable = request.user.UserProfile
    except:
        return HttpResponseRedirect(reverse('login'))
    person_fav = request.user.UserProfile.favourites.all()
    return render(request,'users/homepage/favourites.html',
                          {'person_fav': person_fav })
    
@login_required
def CreateSpecialLineView(request):
    try:
        user = request.user.UserProfile
    except:
        return HttpResponseRedirect(reverse('login'))
    another_special = Special_line.objects.filter(admin_user=user)
    if another_special.exists():
        if not request.GET.get('d',False):
            return HttpResponse(
                'User can have only one line. Please delete existing line.')
        another_special[0].delete()
    
    if request.method == 'POST':
        form = CreateLineForm(request.user,request.POST)
        if form.is_valid():
            print('koko')
            cd = form.cleaned_data
            uniquefield = ''
            print('vfg')
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
                #must be 8 keys..because of join by key
                return ( choice(a) + choice(a) 
                        +choice(a) + choice(a) 
                        +choice(a) + choice(a)
                        +choice(a) + choice(a) )
            while True:
                uniquefield = randomticket()
                if not Special_line.objects.filter(uniquefield=uniquefield).exists():
                    break
            
            line_object = Special_line(name=cd['name'],
                                         information=cd['information'],
                                         instruction=cd['instruction'],
                                         uniquefield=uniquefield,
                                         admin_user=user
                                         
                                         )
            d_o_w=['monday','tuesday',
                   'wednesday','thursday',
                   'friday','saturday','sunday']
            c_d_o_w=['monday','tuesday',
                   'wednesday','thursday',
                   'friday','saturday','sunday']
            for days in d_o_w[:]:
                if cd[days] == False:
                    d_o_w.remove(days)
            error = False
            for days in c_d_o_w:
                x = cd[days[:2]+'_o']
                y = cd[days[:2]+'_c']
                if (x and y ) and x > y and (days in d_o_w):
                    form.add_error(days[:2]+'_o','Line closes before it opens')
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
                return render(request,
                                  'users/special/create_line.html',
                                  {'line_form':form})
            


            today = timezone.now()
            zone = pytz.timezone(user.timezone)
            today = timezone.localtime(today,zone)
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
                    exec_string_open = "line_object."+d_o+"= get_x(cd['"+str(d_o)+"'])"
                    exec_string_close = "line_object."+d_c+"= get_x(cd['"+str(d_c)+"'])"
                    exec(exec_string_open)
                    exec(exec_string_close)
                    days_open.append(each[:2])
           
            line_object.days_open = str(days_open)
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
                    
            
            
            return HttpResponseRedirect (reverse('users:special_detailview'))
           
        else:
            print('invalid')
            return render(request, 'users/special/create_line.html',{'line_form':form})
        
    else:
        form = CreateLineForm(request.user)
        return render(request, 'users/special/create_line.html',{'line_form':form})

@login_required
def EditSpecialLineView(request):
    try:
        user = request.user.UserProfile
    except:
        return HttpResponseRedirect(reverse('login'))
    # the next line means a business shouldn't have two lines with the same name cus slug will be same....Done!
    line = Special_line.objects.get(admin_user=user)
    if request.method == 'POST':    
        form = EditLineForm(request.user,line,request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            zone = pytz.timezone(user.timezone)
            today = timezone.now()
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
                    form.add_error(days[:2]+'_o','Line closes before it opens')
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
                return render(request,'users/special/edit_special_line.html',
                          {'line_form':form,
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
            line.name = cd['name']
            line.information = cd['information']
            line.instruction =  cd['instruction']
            line.save()
            
            return HttpResponseRedirect (reverse('users:special_detailview'))
        else:
            
            return render(request,'users/special/edit_special_line.html',
                          {'line_form':form,
                           'line':line})
    else:
        zone = pytz.timezone(user.timezone)
        today = timezone.now()    
        today = timezone.localtime(today,zone)
        days_open = line.days_open
        days_open = ast.literal_eval(days_open)
        form_data = {'name': line.name,
                'information':line.information,
                'instruction':line.instruction, }#leave comma
        
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
                variabu = (7-all_days[weekdayy]) + wikd
        
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
 
        
        form = EditLineForm(request.user,line,initial=form_data)
        delete_line_form = DeleteBusinessLineForm({'delete':line.uniquefield})
        return render(request,'users/special/edit_special_line.html',
                          {'line_form':form,
                           'delete_line_form':delete_line_form,
                           'line':line,
                           })
        


@login_required
def SpecialLineDetailView(request):
    #for user as business
    user = request.user
    try:
        #just use request user then business to shorten len url
        thebusiness = user.UserProfile
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse('login'))
    try:
        businessline = Special_line.objects.get(admin_user=thebusiness)
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse('users:user_homepage'))
    
    if request.method == 'POST':
        body = request.body.decode('utf-8')
        body = json.loads(body)
        line = businessline.all_present.all().order_by('time')
        for eachuser in line:
            if eachuser.unique == body['remove']:
                if not eachuser.present_line or not eachuser.special_line:
                    eachuser.present_line = None
                    eachuser.special_line = None
                    today = timezone.now()
                    t_spent  = today - eachuser.time
                    days_in_sec = t_spent.days * 86400
                    seconds = t_spent.seconds  
                    eachuser.total_seconds  = eachuser.total_seconds + days_in_sec + seconds
                    eachuser.save()
                    line_changed.send(sender=None,
                                      line_uniquefield=businessline.uniquefield)
        #return something
        return HttpResponse(1)
                
    else:
        today = timezone.now()
        time = today.time()
        open_or_closed='closed'
        all_days = {'mo':1,'tu':2,'we':3,'th':4,'fr':5,'sa':6,'su':7}
        inv_days = {1:'mo',2:'tu',3:'we',4:'th',5:'fr',6:'sa',7:'su'}
        days_open = businessline.days_open
        days_open = ast.literal_eval(days_open)
        tomorrow = False

        #business_local
        zone = pytz.timezone(thebusiness.timezone)
                            
        local_weekday = timezone.localdate(today,zone).isoweekday()
        local_date = timezone.localtime(today,zone)
        iso_days = []
        for all_ in all_days:
            if all_ in days_open:
                iso_days.append(all_days[all_])
        
        model_string = "businessline"       
        def generate(keyy,o=False):
            businessline
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
                # both vx and vy are relevant
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


            
        line = businessline.all_present.all().order_by('time')
        number_of_people = len(line)
        form = RemoveForm()
        
        line = line[:5]
            
        return render (request,
                           'users/special/special_detailview.html',
                           {'businessline': businessline,
                            'line':line,
                            'opentime':opentime,
                            'closetime':closetime,
                            'open_or_closed':open_or_closed,
                            'number_of_people':number_of_people,
                            'the_form':form})

def special_ajax(request):
    user = request.user
    if not user.is_authenticated:
        return HttpResponse('a')
    try:   
        business = user.UserProfile
    except ObjectDoesNotExist:
        return HttpResponse('a')
    line_object = False
    try:
        line_object = user.UserProfile.admin_special_line
    except ObjectDoesNotExist:
        pass
    if not line_object:
        return HttpResponse('r')
    else:
        if business != line_object.admin_user:
            return HttpResponse('a')
        line = line_object.all_present.all().order_by('time')
    compare = request.session.get('admin_compare', None)
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
                    request.session['admin_compare'] = json_line
                    return HttpResponse('*'+y)
            if compare_list == json_list:
                return HttpResponse('-')
        request.session['admin_compare'] = json_line
        return HttpResponse(JsonResponse(json_line))
    else:
        if compare:
            request.session['admin_compare'] = ''
            return HttpResponse(0)
        else:
            return HttpResponse(0)
            
    
    

