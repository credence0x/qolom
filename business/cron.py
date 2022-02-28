from django.core.cache import cache
from django.dispatch import receiver
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from account.tokens import account_activation_token_two
from django.core.mail import send_mail
from django.template import loader
from account.models import Orders,BusinessProfile
from django.utils import timezone
from django.db import transaction
from django.contrib.auth.models import User


def job():
    ###################### SEND EMAIL #############################
    x = User.objects.all()
    for b in x:
        try:
            user = b.UserProfile
            break
        except Exception:
            pass
    order = Orders.objects.all()[0]
    business = order.business    
    mail_subject = 'Cron Job is Ready'
    plain_message = render_to_string('users/payments/order_ready_mail.html',
                            {'user': user,
                            'domain': 'qolom.com',
                             'order':order,
                             'business':business,
                            })
    html_message = loader.render_to_string('users/payments/order_ready_mail.html',
                            {'user': user,
                            'domain': 'qolom.com',
                             'order':order,
                             'business':business,
                            })
    to_email = 'ojetoks@gmail.com'
                       
    send_mail(mail_subject,
                                  plain_message,
                                  'Qolom <auth@qolom.com>',#change
                                  [to_email,],
                                  html_message = html_message,
                                  fail_silently=False)
    
