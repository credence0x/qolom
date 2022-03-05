from logging.config import valid_ident
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings
import re
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from account.tokens import account_activation_token_three,account_activation_token


class Email:
    def __init__(self,request,user) -> None:
        self.current_site = get_current_site(request)
        self.user = user
        self.mail_subject = ""
        self.plain_message = ""
        self.to_email = ""
        self.html_message = ""
            
    
    def __send(self):
        send_mail(self.mail_subject,
                self.plain_message,
                settings.AUTH_FROM_EMAIL,
                [self.to_email,],
                html_message = self.html_message,
                fail_silently=False
                )

                
    def send_common_activation_mail(self):
        """
        Actiation mail to be sent when an account is created
        to prove that they own email address
        """
        user = self.user
        context =  {'user': user,
                    'domain': self.current_site.domain,
                    'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                    'token':account_activation_token.make_token(user),
                    }
        self.mail_subject = 'Activate Your Account.'
        self.to_email = user.email
        self.html_message = render_to_string('account/authentication/confirm_registration.html',context)
        self.plain_message = self.html_message
        self.__send()

        # values are needed for proper testing
        if str(self.current_site)=="testserver":
            return {
                    "uidb64": context.get('uid'),
                    "token":context.get('token')
                }
    def send_common_welcome_mail(self):
        """
        An email sent after successful activation of account
        """
        user = self.user
        context = {'user': user,
                    'domain': self.current_site.domain,
                    }
        self.mail_subject = 'Account Activated'
        
        self.html_message = render_to_string('account/authentication/welcome.html',context)
        self.plain_message = self.html_message
        self.to_email = user.email
        self.__send()



    def send_common_reset_password_mail(self):
        """
        An email sent when a user requests to 
        reset their password
        """
        user = self.user
        context = {'user': user,
                    'domain': self.current_site.domain,
                    'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                    'token':account_activation_token_three.make_token(user),
                }
        self.mail_subject = 'Reset Your Password'
        self.html_message = render_to_string('account/authentication/reset_password_mail.html',context)
        self.plain_message = self.html_message
        self.to_email = user.email    
        self.__send()

        # values are needed for proper testing
        if str(self.current_site)=="testserver":
            return {
                    "uidb64": context.get('uid'),
                    "token":context.get('token')
                }


    

    
    def send_order_ready_mail(self,order):
        """
        Notify buyer that their order is ready
        """
        context =  {'user': order.buyer,
                    'business':order.seller,
                    'domain': self.current_site.domain,
                    'order':order,
                    }
        self.mail_subject = f"Your Order [{order.reference}] is Ready"
        self.to_email = order.buyer
        self.html_message = render_to_string('users/payments/order_ready_mail.html',context)
        self.plain_message = self.html_message
        self.__send()



                
                
                
        

    