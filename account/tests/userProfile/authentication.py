from django.test import Client
from django.urls import reverse
from account.serializers.userProfile import userProfile
from rest_framework import status
from rest_framework.test import APITestCase
from account.models import UserProfile
import datetime,ast
from django.contrib.auth.models import User
from django.contrib import auth



class AuthenticateUserProfileTests(APITestCase):
    def __init__(self, *args, **kwargs):
        super(AuthenticateUserProfileTests, self).__init__(*args, **kwargs)
                        
        self.login_data =  {   
                            "username": "Babatola",
                            "password":"1234@334&*9",
                           }
    
    def __correct_byte(self,byte_value):
        return ast.literal_eval(byte_value.decode('utf-8'))
    
    @classmethod    
    def setUpTestData(cls):
        create_data =      {    "first_name": "Babatola",
                                "last_name":"Ojetokun",
                                "username":"babatola",
                                "email":"babatola@gmail.com",
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
        user.is_active = True
        user.save()
        cls.username = user.username
        cls.password = create_data.get("password")
        cls.url = reverse('account:authenticate_user_profile')

    
   

    def test_authentication_with_correct_username_details(self):
        """
        Ensure that authentication with the correct details works.
        """
        data = self.login_data.copy()
        response = self.client.post(self.url, data, format='json')
        content = self.__correct_byte(response.content)
        user = auth.get_user(self.client)
        self.assertEqual(content.get("password",False),False), f"Password field must not be sent out"
        self.assertEqual(user.is_authenticated,True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_authentication_with_correct_email_details(self):
        """
        Ensure that authentication with the correct details works.
        """
        data = self.login_data.copy()
        data["username"] = "babatola@gmail.com"
        response = self.client.post(self.url, data, format='json')
        content = self.__correct_byte(response.content)
        user = auth.get_user(self.client)
        self.assertEqual(content.get("password",False),False), f"Password field must not be sent out"
        self.assertEqual(user.is_authenticated,True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_authentication_with_wrong_details(self):
        """
        Ensure that wrong authentication details don't work.
        """
        data = self.login_data.copy()
        data['password'] = "wrong_password"
        response = self.client.post(self.url, data, format='json')
        content = self.__correct_byte(response.content)
        user = auth.get_user(self.client)

        self.assertEqual(content.get("password",False),False), f"Password field must not be sent out"
        self.assertEqual(user.is_authenticated,False)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        



    def test_authentication_of_inactive_user(self):
        
        # create test account
        create_account_url = reverse('account:create_user_profile')
        c = Client()
        data = self.create_data
        data["username"]="testing123"
        data["email"]="testing@gmail.com"
        c.post(create_account_url, data , format='json')
        

        # actual test
        response = self.client.post(self.url, data, format='json')
        error = self.__correct_byte(response.content)
        user = auth.get_user(self.client)
        self.assertEqual(error.get("password",False),False), f"Password field must not be sent out"
        assert error.get("account",False) != False, f"An error stating that the account is inactive should pop up"
        self.assertEqual(user.is_authenticated,False)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)









class DeauthenticateUserProfileTests(APITestCase):
    def __init__(self, *args, **kwargs):
        super(DeauthenticateUserProfileTests, self).__init__(*args, **kwargs)
                        
        self.login_data =  {   
                            "username": "Babatola",
                            "password":"1234@334&*9",
                           }
    
    def __correct_byte(self,byte_value):
        return ast.literal_eval(byte_value.decode('utf-8'))
    
    @classmethod    
    def setUpTestData(cls):
        create_data =      {    "first_name": "Babatola",
                                "last_name":"Ojetokun",
                                "username":"babatola",
                                "email":"babatola@gmail.com",
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
        user.is_active = True
        user.save()
        cls.authenticate_url = reverse('account:authenticate_user_profile')
        cls.url = reverse('account:deauthenticate_user_profile')

    
   

    def test_deauthentication(self):
        """
        Ensure that deauthentication works.
        """
        # Authenticate
        data = self.login_data.copy()
        response = self.client.post(self.authenticate_url, data, format='json')
        user = auth.get_user(self.client)
        self.assertEqual(user.is_authenticated,True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        #Deauthenticate
        response = self.client.post(self.url, data, format='json')
        user = auth.get_user(self.client)
        self.assertEqual(user.is_authenticated,False)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
