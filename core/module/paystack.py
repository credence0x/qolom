from django.conf import settings
import requests
from core.module.math import safe_total


class Paystack:
    def __init__(self) -> None:
        self.secret_key = settings.PAYSTACK_SECRET_KEY
        
    def initialize_payment(self,order):
        """
        Initialize payment and 
        send link for final payment
        """
        total_plus_fees = order.total + order.fees

        response = requests.post(
                            'https://api.paystack.co/transaction/initialize',
                            headers={
                                        'Authorization': f'Bearer {self.secret_key}',
                                        'Content-Type': 'application/json'
                                    },
                            json={
                                    'email':order.buyer.user.email,
                                    'amount':safe_total(total_plus_fees)
                                }
                            )

        if response.status_code == 200:   
            if response.json().get('status')==True:                 
                data = response.json().get('data')
                return data
        return False

    

    def verify_payment(self,order):
        """
        Verify payment for order
        """
        
        response = requests.get(
                            f'https://api.paystack.co/transaction/verify/{order.reference}',
                            headers={
                                    'Authorization': f'Bearer {self.secret_key}',
                                }
                            )
    
        if response.status_code==200:
            if response.json().get('status')==True:            
                data = response.json().get('data')
                """
                    note that in order to get the real 
                    transaction status we still have to 
                    get data["status"] which can be 'failed' or 'success'
                """
                return data
                
        return False

    
    # def test_charge(self):
    #     """
    #     test_charge
    #     """
    #     response = requests.post('https://api.paystack.co/charge',
    #                              headers={
    #                                     'Authorization': f'Bearer {self.secret_key}',
    #                                     'Content-Type': 'application/json'
    #                                 },
    #                              json={  
    #                                  "email": "lojetokun@gmail.com", 
    #                                  "amount": "10000",
    #                                  "card":{
    #                                             "number":"",
    #                                             "expiry_month":"",
    #                                             "expiry_year":"",
    #                                             "cvv":"",
    #                                         }
    #                                     })
        
        
    #     if response.status_code == 200:
    #         data = response.json().get('data')
            
    #         status = data.get('status')
    #         if status == 'success':
    #             return data
    #     print(response.json())          
    #     return False



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
                                 json={ "authorization_code" : card.authorization_code,
                                        'email': order.buyer.user.email,
                                        'amount': safe_total(total_plus_fees)
                                        })
        
        
        if response.status_code == 200:
            data = response.json().get('data')
            status = data.get('status')
            if status == 'success':
                return data
                    
        return False    


    ################################ NON PAYMENT APIS ##############################
    
    def resolve_bank(self,account_number,bank_code):
        """
        Get a business' bank account information
        using account number and bank code
        """
        query_params = f"?account_number={account_number}&bank_code={bank_code}"
        response = requests.get('https://api.paystack.co/bank/resolve'+ query_params,
                                    headers={
                                            'Authorization': f'Bearer {self.secret_key}',
                                        }
                                )

        if response.status_code == 200:
            data = response.json().get('data')
            return data
                    
        return False   


    
    def list_banks(self):
        """
        Get list of banks and their information
        """
        response = requests.get('https://api.paystack.co/bank',
                                    headers={
                                            'Authorization': f'Bearer {self.secret_key}',
                                        }
                                )

        if response.status_code == 200:
            data = response.json().get('data')
            return data
                    
        return False   

    def add_transfer_recipient(self,user):
        """
        add transfer recipient to PayStack
        """
        business = user.businessProfile
        bank = business.bank
        response = requests.post('https://api.paystack.co/transferrecipient',
                                 headers={
                                        'Authorization': f'Bearer {self.secret_key}',
                                        'Content-Type': 'application/json'
                                    },
                                 json={ 
                                            "type": "nuban",
                                            "name": f"{business.name}",
                                            "account_number": bank.account_number,
                                            "bank_code": bank.bank_code,
                                            "currency": "NGN"
                                        }
                                )
        
        
        if response.status_code == 201:
            data = response.json().get('data')
            bank.recipient_code = data.get("recipient_code")
            bank.save()
            return True
                    
        return False  
        