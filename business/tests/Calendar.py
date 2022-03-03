from django.test import Client
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
import datetime,ast
from django.contrib.auth import get_user_model
from business.module import variables

User = get_user_model()
   

class CreateCalendarTests(APITestCase):
    def __init__(self, *args, **kwargs):
        super(CreateCalendarTests, self).__init__(*args, **kwargs)
                        
        self.data =  {      "name":"Coffee Queue",
                            "instructions":"Please be available when your turn ",
                            "information":"We only sell coffee here",
                     }
        for day in variables.LIST_OF_DAYS:
            open_time = f"{day}_o"
            closing_time = f"{day}_c"
            self.data[open_time] = datetime.time(13,00,00) # 1:00 PM
            self.data[closing_time] = datetime.time(23,59,59) # 11:59 PM

            

    def __correct_byte(self,byte_value):
        return ast.literal_eval(byte_value.decode('utf-8'))
    
    @classmethod    
    def setUpTestData(cls):
        create_data = {    
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
                        "timezone":"Lagos/Africa"
                    }
        

        url = reverse('account:create_business_profile')
        c = Client()
        c.post(url, create_data, format='json')
        user = User.objects.get(username=create_data.get("username").lower())
        user.is_active = True
        user.save()
        cls.username = user.username
        cls.password = create_data.get("password")
        
    
    def setUp(self):
        self.client.login(username=self.username.lower(),
                            password=self.password)
        



    def test_is_athentication_permission(self):
        """
        Ensure that the user must be logged in order 
        to perform any of the actions relating to this test
        """
        data = self.data.copy()
        c = Client() # and not self.client which is already logged in
        response = c.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_is_business_permission(self):
        """
        Ensure that the user is a business account
        """

        # Create user profile account
        data =  {
                            "first_name": "Lanre",
                            "last_name":"Ojetokun",
                            "username":"Olanrewaju",
                            "email":"lojetokun@gmail.com",
                            "password":"1234@334&*9",
                            "password_2":"1234@334&*9",
                            "d_o_b": datetime.datetime.now().date(),
                            "iso_code":"NG",
                            "country":"Nigeria",
                            "timezone":"Lagos/Africa"    
                }
        response = self.client.post(reverse('account:create_user_profile'), data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(username=data.get("username").lower())
        user.is_active = True
        user.save()

        # actual test
        c = Client() # authenticate new client object with user profile object
        c.login(username=data.get('username').lower(),
                password=data.get('password'))

