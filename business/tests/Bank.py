from email.headerregistry import ContentTypeHeader
from django.test import Client
from django.urls import reverse
from business.models.Queue import BusinessQueue
from rest_framework import status
from rest_framework.test import APITestCase
import datetime
from django.contrib.auth import get_user_model
from business.module import variables
import json

User = get_user_model()

DEFAULT_USER_PROFILE_DATA = {
                                "first_name": "Lanre",
                                "last_name":"Ojetokun",
                                "username":"Olanrewaju",
                                "email":"lojetokun@gmail.com",
                                "password":"1234@334&*9",
                                "password_2":"1234@334&*9",
                                "d_o_b": datetime.datetime.now().date(),
                                "iso_code":"NG",
                                "country":"Nigeria",
                           }

DEFAULT_BUSINESS_PROFILE_DATA = {    
                                    "name": "Starbucks International Ltd",
                                    "username":"starbucks",
                                    "email":"lojetokun2@gmail.com",
                                    "password":"1234@334&*9",
                                    "password_2":"1234@334&*9",     
                                    "minimum_age_allowed":"18",
                                    "iso_code":"NG",
                                    "country":"Nigeria",
                                    "state":"Lagos",
                                    "address":"14, Titi Close, Ogba",
                                }

class BankTests(APITestCase):
    def __init__(self, *args, **kwargs):
        super(BankTests, self).__init__(*args, **kwargs)
                        
        
        

    def __correct_byte(self,byte_value):
        return json.loads(byte_value.decode('utf-8'))
    
    @classmethod    
    def setUpTestData(cls):
        create_data = DEFAULT_BUSINESS_PROFILE_DATA
        

        url = reverse('account:create_business_profile')
        c = Client()
        c.post(url, create_data, format='json')
        user = User.objects.get(username=create_data.get("username").lower())
        user.is_active = True
        user.save()
        cls.user = user
        cls.username = user.username
        cls.password = create_data.get("password")
        
    
    def setUp(self):
        self.client.login(username=self.username.lower(),
                            password=self.password)
        


    def test_list_banks(self):
        """
        Ensure you can get list of banks as well as bank_code
        """
        response = self.client.get(reverse('business:bank_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
       

    def test_resolve_bank(self):
        """
        Ensure that resolve works
        """
        data = {
            "account_number" : "0263051071",
            "bank_code":"058"
        }
        response = self.client.post(reverse('business:bank_resolve'), data , format='json')
        content = self.__correct_byte(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(content["data"]["account_name"],"OJETOKUN OLANREWAJU ADEDOTUN")
        self.assertEqual(content["data"]["account_number"],data.get("account_number"))
        

    def test_bank_add(self):
        """
        Ensure that a business can add a bank account
        """
        data = {
            "owner" : self.user.businessProfile.pk,
            "bank_name":"Guarantee Trust Bank",
            "bank_code":"058",
            "account_number":"0263051071",
            "account_name":"OJETOKUN OLANREWAJU ADEDOTUN",
            "password":self.password
        }
        response = self.client.post(reverse('business:bank_add'), data , format='json')
        content = self.__correct_byte(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        exempt = ["password"]
        for key,value in data.items():
            if key not in exempt:
                self.assertEqual(value,content.get(key))

    


        

        
    def test_bank_confirmation(self):
        """
        Ensure that business can confirm the activation of
        a new bank account to receive money
        """
        # first add an account and get uidb64,token
        add_data = {
            "owner" : self.user.businessProfile.pk,
            "bank_name":"Guarantee Trust Bank",
            "bank_code":"058",
            "account_number":"0263051071",
            "account_name":"OJETOKUN OLANREWAJU ADEDOTUN",
            "password":self.password
        }
        response = self.client.post(reverse('business:bank_add'), add_data , format='json')
        content = self.__correct_byte(response.content)
        uidb64 = content.get("uidb64")
        token = content.get("token")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        

        # actual confirmation test
        confirmation_data = {
            "uidb64" : uidb64,
            "token":token,
        }
        response = self.client.post(reverse('business:bank_confirm'), confirmation_data , format='json')
        content = self.__correct_byte(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        