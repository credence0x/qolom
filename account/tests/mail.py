from django.test import Client
from django.urls import reverse
from account.serializers.userProfile import userProfile
from rest_framework import status
from rest_framework.test import APITestCase
from account.models import UserProfile
import datetime,ast
from django.contrib.auth import get_user_model
from django.contrib import auth
from django.test import override_settings

User = get_user_model()



class SignUpConfirmationEmailTests(APITestCase):
    def __init__(self, *args, **kwargs):
        super(SignUpConfirmationEmailTests, self).__init__(*args, **kwargs)
                        
        self.data =  {   
                        "username": "Babatola",
                   }
        
    
    def __correct_byte(self,byte_value):
        return ast.literal_eval(byte_value.decode('utf-8'))
    
    @classmethod    
    def setUpTestData(cls):
        create_data =      {    "first_name": "Babatola",
                                "last_name":"Ojetokun",
                                "username":"babatola",
                                "email":"lojetokun@gmail.com",
                                "password":"1234@334&*9",
                                "password_2":"1234@334&*9",
                                "d_o_b": datetime.datetime.now().date(),
                                "iso_code":"NG",
                                "country":"Nigeria",
                                "timezone":"Lagos/Africa"
                         }
        cls.create_data = create_data
        url = reverse('account:create_user_profile')
        c = Client()
        c.post(url, create_data, format='json')
        user = User.objects.get(username=create_data.get("username").lower())
        cls.username = user.username
        cls.password = create_data.get("password")
        cls.url = reverse('account:mail_confirm_sign_up')



    def setUp(self):
        self.client.login(username=self.username.lower(),
                            password=self.password)
        

    
   
    # @override_settings(EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend')
    def test_send_email_with_valid_username(self):
        """
        Ensure that email is sent with the correct details works.
        """
        data = self.data.copy()
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    



    def test_send_email_with_invalid_username(self):
        """
        Ensure that email is sent with the correct details works.
        """
        data = self.data.copy()
        data["username"]="random_username"
        response = self.client.post(self.url, data, format='json')
        error = self.__correct_byte(response.content)
        assert error.get('username',False) !=  False, f"Invalid username error should pop up"
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)





    def test_send_email_with_active_user(self):
        """
        Ensure that email is not sent to active users
        """
        data = self.data.copy()
        user = User.objects.get(username=data.get("username").lower())
        user.is_active = True
        user.save()
        response = self.client.post(self.url, data, format='json')
        error = self.__correct_byte(response.content)
        assert error.get('account',False) !=  False, f" Active account error should pop up"
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)