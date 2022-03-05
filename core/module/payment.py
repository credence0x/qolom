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
            response = requests.post(
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
        if response.json().get('status')==False:
            return False
                 
        data = response.json().get('data')
        return data


    def pay_with_card(self,order,card):
        """
        Implementation of payment with saved card
        """
        total_plus_fees = order.total + order.fees
        response = requests.post('https://api.paystack.co/transaction/charge_authorization',
                                 headers={
                                        'Authorization': f'Bearer {self.secret_key}',
                                        'Content-Type': 'application/json'
                                    },
                                 json={ "authorization_code" : card,
                                        'email': order.buyer.email,
                                        'amount': total_plus_fees,
                                        })
        
        
        if response.status_code == 200:
            data = response.json().get('data')
            status = data.get('status')
            if status == 'success':
                return data
                    
        return False     