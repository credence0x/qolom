from django.shortcuts import render,redirect
from .forms import CreateUserAccountForm, BusinessAccountForm,ChangeEmailForm,PasswordResetForm,new_passwordForm,LoginForm,EditBusinessProfileForm
from account.models import UserProfile,BusinessProfile
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import HttpResponse,HttpResponseRedirect
import datetime
from random import choice
from django.urls import reverse
from django.contrib.auth import logout
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from .tokens import account_activation_token,account_activation_token_three
from django.core.mail import send_mail
import re
from django.template import loader
from io import BytesIO
from PIL import Image
from django.core.files import File
from django.contrib import messages
from django.db import IntegrityError



def UserAccountView(request):
    if request.method == 'POST':
        x = request.GET.get('p',None)
        form = CreateUserAccountForm(request.POST)
        if form.is_valid():
            keep_tab = 0
            while True:
                try:  
                    cd = form.cleaned_data
                    def randomticket():
                        a = ['A','B','C','D','E','F','G','H',
                             'I','J','K','L','M','N','O','P',
                             'Q','R','S','T','U','V','W','X',
                             'Y','Z','1','2','3','4','5','6',
                             '7','8','9','0']
                        #shorter than using a for loop
                        return ( choice(a)+ choice(a)
                                +choice(a)+ choice(a)
                                +choice(a)+ choice(a))
                    
                    ticket = randomticket()
                    def getKey():
                        b = ['A','B','C','D','E','F','G','H',
                             'I','J','K','L','M','N','P',
                             'Q','R','S','T','U','V','W','X',
                             'Y','Z','a','b','c','d','e','f',
                             'g','h','i','j','k','m','n',
                             'p','q','r','s','t','u','v',
                             'w','x','y','z','2','3','4',
                             '5','6','7','8','9']
                        # no 0,o,O,1,l to avoid confusion
                        # key must be 7
                        return ( choice(b) + choice(b) 
                                +choice(b) + choice(b) 
                                +choice(b) + choice(b)
                                +choice(b))
                    while True:
                        key=getKey()
                        if not User_signup.objects.filter(unique=key).exists():
                            break
                    user = User.objects.create_user(username=cd['username'],
                                        password=cd['password'],
                                        first_name=cd['first_name'],
                                        last_name=cd['last_name'],
                                        email = cd['email'],
                                        is_active=False
                                        )
                    
                    second_obj = User_signup.objects.create(user=user,
                                               first_name=cd['first_name'],
                                               last_name=cd['last_name'],
                                               country=cd['country'],
                                               iso_code=cd['iso_code'],
                                               timezone = cd['timezone'],
                                               age=cd['date_of_birth'],
                                               unique=key,
                                               ticket = ticket,
                                               total_seconds=0
                                               )
                    request.session['temp_user'] = cd['username']
                    return HttpResponseRedirect(reverse('account:confirm_html'))
                except IntegrityError:
                    if user:
                        user.delete()
                    if second_obj:
                        second_obj.delete()
                    if keep_tab == 2:
                        form.add_error('username','something went wrong')
                        return render(request,
                                      'account/registration/usersignup.html',
                                      {'form': form})
                        break
                    keep_tab +=1
        else:
            return render(request,
                          'account/registration/usersignup.html',{'form':form})

    else:
        form = CreateUserAccountForm()
        return render(request,
                      'account/registration/usersignup.html',
                      {'form':form})

def BusinessAccountView(request):
    if request.method == 'POST':
        form = BusinessAccountForm(request.POST)
        if form.is_valid():
            keep_tab = 0
            while True:
                try:
                    
                    cd = form.cleaned_data
                    # print (cd['minimum_age'])
                    # return
                    user = User.objects.create_user(username=cd['username'],
                                        password=cd['password'],
                                        first_name=cd['name'],
                                        email = cd['email'],
                                        is_active=False
                                        )
                    
                    def getKey():
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
                    
                    while True:
                        key = getKey()
                        if not Business_signup.objects.filter(key=key).exists():
                            break
                    
                    second_obj = Business_signup.objects.create(user=user,
                                                   name=cd['name'],
                                                   address = cd['address'],
                                                   state = cd['state'],
                                                   country = cd['country'],
                                                   iso_code = cd['iso_code'],
                                                   timezone = cd['timezone'],
                                                   min_age = cd['minimum_age'],
                                                   key=key
                                                   )
                    request.session['temp_user'] = cd['username']
                    return HttpResponseRedirect(reverse('account:confirm_html'))
                    break
                except IntegrityError:
                    if second_obj:
                        second_obj.delete()
                    if user:
                        user.delete()
                    if keep_tab == 2:
                        form.add_error('name','something went wrong')
                        return render(request,
                                      'account/registration/businesssignup.html',
                                      {'form': form})
                        break
                    keep_tab +=1
                    
        else:
            return render(request, 'account/registration/businesssignup.html', {'form': form})
    else:
        form = BusinessAccountForm()
        return render(request, 'account/registration/businesssignup.html',
                      {'form': form })

def ResetPasswordView(request):
    if request.method=='POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            try:
                user = User.objects.get(username=cd['username'])
            except User.DoesNotExist:
                try:
                    user = User.objects.get(email=cd['username'])
                except User.DoesNotExist:
                    # no nedd for .lower()...taken care of in forms
                    form.add_error('username','No user with that username or email exists ')
                    return render(request,'account/authentication/forgot_password.html',
                                  {'reset_form':form})
            current_site = get_current_site(request)
            mail_subject = 'Reset Your Password'
            plain_message = render_to_string('account/authentication/reset_password_mail.html',
                {'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token_three.make_token(user),
                })
            html_message = loader.render_to_string('account/authentication/reset_password_mail.html',
                                  {'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token_three.make_token(user),
                })
            to_email = user.email
            # to_email = "support@qolom.com"
            
            send_mail(mail_subject,
                      plain_message,
                      'Qolom <support@qolom.com>',
                      [to_email,],
                      html_message = html_message,
                      fail_silently=False)
            sent=True
            mail_split = re.split('@',user.email)
            mail = mail_split[0]
            ext = mail_split[1]
            return render(request,'account/authentication/forgot_password.html',
                              {'sent':sent,
                               'mail':mail,
                               'ext':ext})
        else:
            form = PasswordResetForm()
            return render(request,'account/authentication/forgot_password.html',
                          {'reset_form':form})
    else:
        form = PasswordResetForm()
        return render(request,'account/authentication/forgot_password.html',
                          {'reset_form':form})

        
def activate_resetView(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token_three.check_token(user, token):
        return HttpResponseRedirect(reverse('account:set_new_password',
                                            args=[uidb64,token]))
    else:
        
        return HttpResponseRedirect(reverse('login') + '?u=invalid-forgot')
        


    
def set_new_passwordView(request,uidb64,token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token_three.check_token(user, token):
        
        if request.method=='POST':
            form = new_passwordForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                user.set_password(cd['password1'])
                user.save()
                return HttpResponseRedirect(reverse('login') + '?u=fsuccess')
            else:
                return render(request,'account/authentication/set_new_password.html',
                          {'new_passwordForm':form})
        else:
            form = new_passwordForm()
            return render(request,'account/authentication/set_new_password.html',
                          {'new_passwordForm':form})
    else:
        return HttpResponseRedirect(reverse('login') + '?u=invalid-forgot')
            
            
def confirm_emailView(request):
    username = request.session['temp_user']
    try:
        if '@' and '.' in username:
            user = User.objects.get(email=username)
        else:
            user = User.objects.get(username=username)
    except ObjectDoesNotExist:
        try:
            user = User.objects.get(username=username)
        except ObjectDoesNotExist:
            messages.error(request,'Something went wrong')
            return HttpResponseRedirect(reverse('login'))
            
    if user.is_active==False:
        x = request.GET.get('p',None)        
        current_site = get_current_site(request)
        mail_subject = 'Activate Your Account.'
        plain_message = render_to_string('account/authentication/confirm_registration.html', {
            'user': user,
            'domain': current_site.domain,
            'uid':urlsafe_base64_encode(force_bytes(user.pk)),
            'token':account_activation_token.make_token(user),
            })
        to_email = user.email
        html_message = loader.render_to_string('account/authentication/confirm_registration.html',
                {'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
                })
        print('http://localhost:8000/'+
              urlsafe_base64_encode(force_bytes(user.pk))+
              '/'+account_activation_token.make_token(user))
        #from validate_email import validate_email
        '''is_valid = validate_email(email_address='ojetnoks@gmail.com',
                                  check_regex=True,
                                  check_mx=True,
                                  smtp_timeout=5,
                                  dns_timeout=5,
                                  use_blacklist=True,
                                  debug=False)
        return HttpResponse(is_valid)'''
        send_mail(mail_subject,
                  plain_message,
                  'Qolom <auth@qolom.com>',
                  [to_email,],
                 html_message = html_message,
                 fail_silently=False)
        
        if x == 'x':
            return HttpResponse('-')
        return render(request,'account/authentication/confirm_email.html',
                      {'email':user.email})
    else:
        return HttpResponse("your account is already active")

def changeEmail(request):
    username = request.session.get('temp_user',False)
    if username and not request.user.is_authenticated:
        try:
            user = User.objects.get(username=username)
        except Exception:
            return HttpResponse('Something went wrong.')
        if user.is_active:
            return HttpResponseRedirect(reverse('login'))
    else:
        return HttpResponseRedirect(reverse('login'))
    
    if request.method == 'POST':
        form = ChangeEmailForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            email = cd['email']
            try:
                x = user.business_signup
                x.email=email
                x.save()
                user.email=email
                user.save()
                return HttpResponseRedirect(reverse('account:confirm_html'))
            except Exception:
                try:
                    x = user.user_signup
                    x.email=email
                    x.save()
                    user.email=email
                    user.save()
                    return HttpResponseRedirect(reverse('account:confirm_html'))
                except Exception:
                    form.add_error('email','something went wrong')
                    return render(request,'account/authentication/change_email.html',
                          {'form':form} )
        else:
            return render(request,'account/authentication/change_email.html',
                          {'form':form} )
    else:
        form = ChangeEmailForm()
        return render(request,'account/authentication/change_email.html',
                          {'form':form} )
    
                        
            

        
def activateView(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        try:
            dsd = user.business_signup
            business = True
        except Exception:
            try:
                sds = user.user_signup
                business = False
            except Exception:
                return HttpResponse('something went wrong')
        user.save()
        current_site = get_current_site(request)
        mail_subject = 'Account Activated'
        plain_message = render_to_string('account/authentication/welcome.html',
                {'user': user,
                'domain': current_site.domain,
                'business':business,
                })
        html_message = loader.render_to_string('account/authentication/welcome.html',
                {'user': user,
                'domain': current_site.domain,
                'business':business,
                })
        to_email = user.email
        send_mail(mail_subject,
                      plain_message,
                      'Qolom <auth@qolom.com>',
                      [to_email,],
                      html_message = html_message,
                      fail_silently=True)
            
        return HttpResponseRedirect(reverse('login') + '?u=vrsf')
    else:
        
        
        return HttpResponseRedirect(reverse('login') + '?u=invalid-reg')
        

def EditBusinessProfileView(request):
    user = request.user
    try:
        business = user.business_signup
    except Exception:
        return HttpResponseRedirect(reverse('login'))
    first_letter = business.name[0]
    if request.method == 'POST':
        edit_business_profile_form = EditBusinessProfileForm(request.user,
                                                             request.POST,
                                                             request.FILES)
        def compress(image):
            im = Image.open(image)
            if im.mode != 'RGB':
                im = im.convert('RGB')
            # create a BytesIO object
            im_io = BytesIO()
            im = im.resize( (300,300),Image.ANTIALIAS ) 
            # save image to BytesIO object
            im.save(im_io, 'JPEG', quality=70) 
            # create a django-friendly Files object
            new_image = File(im_io, name=image.name)
            return new_image

        
        
        if edit_business_profile_form.is_valid():
            cd = edit_business_profile_form.cleaned_data
            user.first_name=cd['name']
            user.save()
            if cd['remove_logo']:
                business.dp=None
            if cd['dp']:
                business.dp = compress(cd['dp'])
            business.name=cd['name']
            business.address = cd['address']
            business.state = cd['state']
            business.country = cd['country']
            business.iso_code = cd['iso_code']
            business.timezone = cd['timezone']
            business.min_age=cd['minimum_age']
            business.save()
            messages.success(request,
                             'Your profile was updated successfully!')
            return HttpResponseRedirect (reverse('business:business_homepage'))
        else:
            # remember to change user edit form to account not user
            return render(request,'account/edit_registration/edit_business_profile.html',
                          {'edit_business_profile_form':edit_business_profile_form} )
    else:
        data = {'name':business.name,
                'address':business.address,
                'state':business.state,
                'iso_code':business.iso_code,
                'timezone':business.timezone,
                'country':business.country,
                'minimum_age':business.min_age
                }
        
        edit_business_profile_form = EditBusinessProfileForm(request.user,
                                                             initial=data)
        return render(request,'account/edit_registration/edit_business_profile.html',
                          {'edit_business_profile_form':edit_business_profile_form,
                           'first_letter':first_letter} )
        
        
        
            
            
                         
    
    


# from django.views.decorators.csrf import csrf_exempt

# @csrf_exempt            
def LoginView(request):
   
    
    if request.method == 'POST':

        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            #not using auth cus it rjectts inactive users
            if '@' and '.' in cd['username']:
                try:
                    user = User.objects.get(email=cd['username'])
                except User.DoesNotExist:
                    try:
                        user = User.objects.get(username=cd['username'])
                    except User.DoesNotExist:
                        form.add_error('username','Username and password did not match')
                        return render(request,
                          'account/authentication/login.html',
                          {'form': form})
            else:
                try:
                    user = User.objects.get(username=cd['username'])
                except User.DoesNotExist:
                    form.add_error('username','Username and password did not match')
                    return render(request,
                          'account/authentication/login.html',
                          {'form': form})
                
            checker = user.check_password(cd['password'])
            if user.is_active and checker:
                
                try:
                    business_user = user.business_signup
                    login(request, user)
                    next_page = request.session.get('next_page',False)
                    if next_page:
                        del request.session['next_page']
                        return HttpResponseRedirect(next_page)
                    return HttpResponseRedirect(reverse('business:business_homepage'))
                except Exception:
                    pass
                
                    
                try:
                    normal_user = user.user_signup
                    login(request, user)
                    next_page = request.session.get('next_page',False)
                    if next_page:
                        del request.session['next_page']
                        return HttpResponseRedirect(next_page)
                    return HttpResponseRedirect(reverse('users:user_homepage'))
                except Exception:
                    #admin 
                    form.add_error('username','Username and password did not match')
                    return render(request,
                          'account/authentication/login.html',
                          {'form': form})
            elif user.is_active==False and checker:
                request.session['temp_user']=cd['username']
                return render(request,'account/authentication/confirm_email.html',
                              {'email':user.email})
            elif user and not checker:
                form.add_error('username','Username and password did not match')
                return render(request,
                          'account/authentication/login.html',
                          {'form': form})
            else:
                #not supposed to be possible
                return HttpResponse('Disabled Account')
        else:
            return render(request,
                          'account/authentication/login.html',
                          {'form': form})
    else:
        message = request.GET.get('u',False)
        if message:
            # this works better than adding message to redirect as messages dont
            # show on gmail browser 
            if message == 'vrsf': 
                messages.success(request,
                            'Verification successful. Please sign-in ')
            elif message == 'invalid-forgot':
                messages.error(request,
                            'Reset link is no longer valid')
            elif message == 'fsuccess':
                messages.success(request,
                                 'Your password was updated successfully')
            elif message == 'invalid-reg':
                messages.error(request,
                            'Activation link is no longer valid. Sign-in and resend the link')
     
        
        form = LoginForm()
        next_page = request.GET.get('next',False)
        request.session['next_page'] = next_page
        return render(request,
                    'account/authentication/login.html',
                    {'form': form})
        

def LandingPageView(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            try:
                user = request.user.user_signup
                return HttpResponseRedirect(reverse("users:user_homepage"))

            except Exception:
                try:
                    business = request.user.business_signup
                    return HttpResponseRedirect(reverse("business:business_homepage"))

                except Exception:
                    return HttpResponse("No associated User or Business object") 
        else:
            return render(request,'users/landing_page.html')


def LogoutView(request):
    logout(request)
    return HttpResponseRedirect(reverse('landing-page'))

def termsView(request):
    return render(request,'account/terms/terms_of_use.html')
def privacyView(request):
    return render(request,'account/terms/privacy_policy.html')
        
