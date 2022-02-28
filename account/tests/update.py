from django.test import Client
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
import datetime,ast
from django.contrib.auth import get_user_model
from django.test import override_settings


User = get_user_model()


class ResetPasswordTests(APITestCase):
    def __init__(self, *args, **kwargs):
        super(ResetPasswordTests, self).__init__(*args, **kwargs)
        
        
        self.url = reverse('account:reset_password')
        self.mail_url = reverse('account:reset_password_mail')
        self.validation_url = reverse('account:reset_password_link_check')


    @classmethod    
    def setUpTestData(cls):
        create_data =      {    "first_name": "Babatola",
                                "last_name":"Ojetokun",
                                "username":"Babatola",
                                "email":"Lojetokun@gmail.com",
                                "password":"1234@334&*9",
                                "password_2":"1234@334&*9",
                                "d_o_b": datetime.datetime.now().date(),
                                "iso_code":"NG",
                                "country":"Nigeria",
                                "timezone":"Lagos/Africa"
                         }
        # assertions are to ensure that the test app automatically lowers the values
        assert create_data.get('username') != create_data.get('username').lower()
        assert create_data.get('email') != create_data.get('email').lower()


        cls.create_data = create_data
        url = reverse('account:create_user_profile')
        c = Client()
        c.post(url, create_data, format='json')
        cls.username = create_data.get("username").lower()
        cls.email = create_data.get("email").lower()
                
        
    
   
    def __correct_byte(self,byte_value):
        return ast.literal_eval(byte_value.decode('utf-8'))
        
   
   
    # @override_settings(EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend')
    def test_reset_password_mail_using_username_or_email(self):
        """
        Ensure we can send reset password mail to user
        """
        data = [self.username,self.email]
        for value in data:
            new_data = {"username":value}
            response = self.client.post(self.mail_url, new_data, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_reset_password_link_validation_with_wrong_link(self):
        uidb64,token = "wrong","wrong"
        query_params = f"?uidb64={uidb64}&token={token}"
        validation_response = self.client.get(self.validation_url + query_params)
        self.assertEqual(validation_response.status_code, status.HTTP_400_BAD_REQUEST)




    def test_reset_password_link_validation_with_correct_link(self):
        response = self.client.post(self.mail_url, {"username":self.username}, format='json')
        content = self.__correct_byte(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        uidb64,token = content.get("uidb64"),content.get("token")
        query_params = f"?uidb64={uidb64}&token={token}"
        validation_response = self.client.get(self.validation_url + query_params)
        self.assertEqual(validation_response.status_code, status.HTTP_200_OK)

    def test_reset_password_with_wrong_password_2(self):
        data = {"password":"uyawgd&8dhwq",
                "password_2": "uyawgd&8dhwq3"}
        
        response = self.client.post(self.mail_url, {"username":self.username}, format='json')
        content = self.__correct_byte(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        uidb64,token = content.get("uidb64"),content.get("token")
        query_params = f"?uidb64={uidb64}&token={token}"
        reset_response = self.client.post((self.url + query_params),data,format="json")
        reset_error = self.__correct_byte(reset_response.content)
        self.assertIn('password',reset_error, "Password field must return an error")
        self.assertEqual(reset_response.status_code, status.HTTP_400_BAD_REQUEST)



    def test_reset_password_with_correct_passwords(self):
        """
        Ensure we can send reset password mail to user
        """
        data = {"password":"uyawgd&8dhwq"}
        data["password_2"] = data.get("password")
        
        response = self.client.post(self.mail_url, {"username":self.username}, format='json')
        content = self.__correct_byte(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        uidb64,token = content.get("uidb64"),content.get("token")
        query_params = f"?uidb64={uidb64}&token={token}"
        reset_response = self.client.post((self.url + query_params),data,format="json")
        # reset_content = self.__correct_byte(reset_response.content)
        self.assertEqual(reset_response.status_code, status.HTTP_200_OK)

        

    

