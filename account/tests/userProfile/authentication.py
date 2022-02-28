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

# def test_authentication_with_related_business_profile_account(self):
    #     """
    #     Ensure that authentication with a User account that 
    #     doesn't have a related UserProfile object doesn't work.
    #     """
        
class AuthenticateUserProfileTests(APITestCase):
    def __init__(self, *args, **kwargs):
        super(AuthenticateUserProfileTests, self).__init__(*args, **kwargs)
                        
        self.login_data =  {   
                            "username": "Babatola",
                            "email":"Babatola@gmail.com",
                            "password":"1234@334&*9",
                           }
        username = self.login_data.get("username")
        email = self.login_data.get("email")
        self.assertNotEqual(username.lower(), username, "This is to ensure that the value is converted to lowercase during validation ")
        self.assertNotEqual(email.lower(), email, "This is to ensure that the value is converted to lowercase during validation ")

    
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
        Ensure that authentication with emails also.
        """
        data = self.login_data.copy()
        data["username"] = data.get("email")
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
        self.assertEqual(error.get("password",False),False, f"Password field must not be sent out")
        self.assertNotEqual(error.get("account",False),False, f"An error stating that the account is inactive should pop up")
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








      
class ActivateUserProfileTokenTests(APITestCase):
    def __init__(self, *args, **kwargs):
        super(ActivateUserProfileTokenTests, self).__init__(*args, **kwargs)
                        
        self.login_data =  {   
                            "username": "Babatola",
                            "email":"lojetokun@gmail.com",
                            "password":"1234@334&*9",
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
        # create account
        cls.create_data = create_data
        url = reverse('account:create_user_profile')
        c = Client()
        c.post(url, create_data, format='json')

        

    
   
    # @override_settings(EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend')
    def test_activation_of_user_profile_account(self):
        """
        Ensure that activation using the link sent via email works.
        """
        # send confirmation mail to get uidb64 and token
        email_data = {'username':self.create_data.get('username')}
        email_confirmation_url = reverse('account:mail_confirm_sign_up') 

        res_send_confirmation_mail = self.client.post(email_confirmation_url, email_data, format='json')
        content = self.__correct_byte(res_send_confirmation_mail.content)
        uidb64 = content.get('uidb64','')
        token = content.get('token','')
        query_params = f"?uidb64={uidb64}&token={token}"
        url = reverse('account:activate_user_profile') + query_params


        # test activation itself

        response = self.client.get(url)
        content = self.__correct_byte(response.content)
        
        user = User.objects.get(**email_data)
        self.assertEqual(user.is_active,True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_activation_with_wrong_token(self):
        """
        Ensure that activation using the wrong details doesn't work
        """
        # send confirmation mail to get uidb64 and token
        email_data = {'username':self.create_data.get('username')}
        email_confirmation_url = reverse('account:mail_confirm_sign_up') 
        res_send_confirmation_mail = self.client.post(email_confirmation_url, email_data, format='json')
        content = self.__correct_byte(res_send_confirmation_mail.content)
        uidb64 = content.get('uidb64','')
        token = "WRONG_TOKEN"
        query_params = f"?uidb64={uidb64}&token={token}"
        url = reverse('account:activate_user_profile') + query_params


        # test activation itself
        response = self.client.get(url)
        content = self.__correct_byte(response.content)    
        user = User.objects.get(**email_data)
        self.assertEqual(user.is_active,False)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_activation_with_wrong_uidb64(self):
        """
        Ensure that activation using the wrong details doesn't work
        """
        # send confirmation mail to get uidb64 and token
        email_data = {'username':self.create_data.get('username')}
        email_confirmation_url = reverse('account:mail_confirm_sign_up') 
        res_send_confirmation_mail = self.client.post(email_confirmation_url, email_data, format='json')
        content = self.__correct_byte(res_send_confirmation_mail.content)
        uidb64 = "WRONG_UIDB64"
        token = content.get('uidb64','')
        query_params = f"?uidb64={uidb64}&token={token}"
        url = reverse('account:activate_user_profile') + query_params


        # test activation itself
        response = self.client.get(url)
        content = self.__correct_byte(response.content)
        user = User.objects.get(**email_data)
        self.assertEqual(user.is_active,False)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)