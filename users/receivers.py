from django.core.cache import cache
from django.dispatch import receiver
from .signals import line_changed,notify,notify_business,confirm_bank
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from account.tokens import account_activation_token_two
from django.core.mail import send_mail
from django.template import loader
from account.models import BusinessProfile
from business.models import Order
from django.utils import timezone
from django.db import transaction


@receiver(line_changed)
def remove(sender, **kwargs):
    key=kwargs['line_uniquefield']
    cache.delete(key)


    
@receiver(notify)
def notify_user_about_order(sender, **kwargs):
    key=kwargs['key']
    collected=kwargs['collected']
    
    with transaction.atomic():
        order = (
              Orders.objects
                .select_for_update()
                  .get(id=key)
                      )
             
        if collected == True:
            if order.order_status!='COLLECTED':#This prevents major fraud if they back page
                if 'REFUND' not in order.order_status:
                    order.order_status = 'COLLECTED'
                    order.save()
                    with transaction.atomic():
                        business = (
                              Business_signup.objects
                              .select_for_update()
                              .get(id=order.business.id)
                          )
                        dy = ''
                        for b in order.total:
                            if b !=',':
                                dy+=b
                        xc = dy.split('.')
                        business.total_earned = business.total_earned + int(xc[0])
                        business.save()
            return
        else:
            if order.order_status == 'SENT':
                ###################### SEND EMAIL #############################
                request = kwargs['request']
                user = order.user
                business = order.business
                
                current_site = get_current_site(request)
                mail_subject = 'Your Order ['+order.reference+'] is Ready'
                plain_message = render_to_string('users/payments/order_ready_mail.html',
                            {'user': user,
                            'domain': current_site.domain,
                             'order':order,
                             'business':business,
                            })
                html_message = loader.render_to_string('users/payments/order_ready_mail.html',
                            {'user': user,
                            'domain': current_site.domain,
                             'order':order,
                             'business':business,
                            })
                to_email = user.user.email
           
                send_mail(mail_subject,
                                  plain_message,
                                  'Qolom <auth@qolom.com>',#change
                                  [to_email,],
                                  html_message = html_message,
                                  fail_silently=False)
                order.order_status = 'READY'
                order.ready_time = timezone.now()
                order.save()
            else:
                return
        



@receiver(notify_business)
def notify_bus(sender, **kwargs):
    business = kwargs['business']
    business.has_orders = True
    business.save()


@receiver(confirm_bank)
def confam(sender, **kwargs):
    user=kwargs['user']
    request = kwargs['request']
    current_site = get_current_site(request)
    mail_subject = 'Confirm Bank Information'
    plain_message = render_to_string('account/authentication/confirm_bank_mail.html',
                        {'user': user,
                        'domain': current_site.domain,
                        'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                        'token':account_activation_token_two.make_token(user),
                        })
    html_message = loader.render_to_string('account/authentication/confirm_bank_mail.html',
                                          {'user': user,
                        'domain': current_site.domain,
                        'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                        'token':account_activation_token_two.make_token(user),
                        })
    to_email = user.email
                    
    send_mail(mail_subject,
                              plain_message,
                              'Qolom <auth@qolom.com>',
                              [to_email,],
                              html_message = html_message,
                              fail_silently=True)


































