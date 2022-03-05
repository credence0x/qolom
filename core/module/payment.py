from django.conf import settings
import requests


class Paystack:
    def __init__(self) -> None:
        self.secret_key = settings.PAYSTACK_SeCRET_KEY
        
    def initialize_payment(self,order):
        """
        Initialize payment and 
        send link for final payment
        """
        total_plus_fees = order.total + order.fees
        try:
            init_payment = requests.post(
                            'https://api.paystack.co/transaction/initialize',
                            headers={
                                        'Authorization': f'Bearer {self.secret_key}',
                                        'Content-Type': 'application/json'
                                    },
                            json={
                                    'email':order.buyer.email,
                                    'amount':total_plus_fees
                                }
                            )
            
        except:
            return False
        if init_payment.json()['status']==False:
            return False
                 
        data = init_payment.json()['data']
        return data


    def pay_with_card(self,order):
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