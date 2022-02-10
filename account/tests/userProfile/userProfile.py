from django.test import Client
from django.urls import reverse
from account.serializers.userProfile import userProfile
from rest_framework import status
from rest_framework.test import APITestCase
from account.models import UserProfile
import datetime,ast
from django.contrib.auth.models import User


class CreateUserProfileTests(APITestCase):
    def __init__(self, *args, **kwargs):
        super(CreateUserProfileTests, self).__init__(*args, **kwargs)
        self.data =  {      "first_name": "Lanre",
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
        self.url = reverse('account:create_user_profile')
    
    def __correct_byte(self,byte_value):
        return ast.literal_eval(byte_value.decode('utf-8'))
        
   
   

    def test_create_user_profile(self):
        """
        Ensure we can create a new user profile object.
        """
        data = self.data.copy()
        response = self.client.post(self.url, data, format='json')
        content = self.__correct_byte(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(content.get("ticket")), 6)

        user_field_list = ["first_name",
                            "last_name",
                            "username",
                            "email",
                            ]
        for each in user_field_list:
            # assert that the correct values were actually inserted
            assert data[each].lower() == content['user'][each].lower(), f"{data[each]} is not equal {content['user'][each]}"

        user = User.objects.get(username=self.data['username'].lower())
        correct_password = user.check_password(self.data["password"])
        assert correct_password == True
        
        
        userProfile_field_list = ["country",
                            "iso_code",
                            "timezone",
                            "d_o_b",
                            ]
        for each in userProfile_field_list:
            # assert that the correct values were actually inserted            
            assert str(data[each]) == content[each], f"{data[each]} is not equal {content[each]}"


        

    



    def test_field_availability(self):
        """
        Ensure that all mandantory field values are collected 
        """
        data_copy = self.data.copy()
        for key,value in self.data.items():
            data_copy.pop(key)

            response = self.client.post(self.url, data_copy, format='json')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            
            content = self.__correct_byte(response.content)       
            assert key in content, f'"{key}" should be a mandatory field in UserProfile model'
            # return the key value pair to the original dict
            data_copy[key]= value




    def test_validation(self):
        """
        Ensure that all field validations work
        """
        data = self.data.copy()
        data["username"] = "lanre"
        data["password"] = "1234"

        response = self.client.post(self.url, data, format='json')
        error = self.__correct_byte(response.content)
        assert "username" in error, f' Username should have up to 6 characters'
        assert "password" in error, f' Passwords must have up to 8 characters and a special character'
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        data["username"] = "lanre@ojetokun"
        data["password"] = self.data.get("password")

        response = self.client.post(self.url, data, format='json')
        error = self.__correct_byte(response.content)
        assert "@" in error["username"][0], f"Username must not contain the '@' symbol"
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        

        data["username"] = self.data.get("username")
        data["password"] = self.data.get("password")
        data["password_2"] = "please_work"

        response = self.client.post(self.url, data, format='json')
        content = self.__correct_byte(response.content)
        self.assertEqual(content["non_field_errors"][0], 'Passwords did not match')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)



















class UpdateUserProfileTests(APITestCase):
    def __init__(self, *args, **kwargs):
        super(UpdateUserProfileTests, self).__init__(*args, **kwargs)
                        
        self.data =  {      "first_name": "Babatola",
                            "last_name":"Obayemi",
                            "password":"1234@334&*9",
                            "iso_code":"NG",
                            "country":"Nigeria",
                            "timezone":"Lagos/Africa"
                     }
    
    def __correct_byte(self,byte_value):
        return ast.literal_eval(byte_value.decode('utf-8'))
    
    @classmethod    
    def setUpTestData(cls):
        create_data =  {      "first_name": "Lanre",
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
        url = reverse('account:create_user_profile')
        c = Client()
        c.post(url, create_data, format='json')
        user = User.objects.get(username=create_data.get("username").lower())
        user.is_active = True
        user.save()
        cls.username = user.username
        cls.password = create_data.get("password")
        cls.url = reverse('account:update_user_profile',kwargs={'pk': user.userProfile.pk})

    
    def setUp(self):
        self.client.login(username=self.username.lower(),
                            password=self.password)
        



    def test_authentication(self):
       data = self.data.copy()
       c = Client()
       response = c.put(self.url, data, format='json')
       self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
   
   
    def test_update_user_profile(self):
        """
        Ensure we can update user profile object.
        """
        data = self.data.copy()
        response = self.client.put(self.url, data, format='json')
        content = self.__correct_byte(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
        user_field_list = ["first_name",
                            "last_name",
                            ]
        for each in user_field_list:
            # assert that the correct values were actually inserted
            assert data[each].lower() == content['user'][each].lower(), f"{data[each]} is not equal {content['user'][each]}"

        
        
        userProfile_field_list = ["country",
                            "iso_code",
                            "timezone",
                            ]
        for each in userProfile_field_list:
            # assert that the correct values were actually inserted            
            assert str(data[each]) == content[each], f"{data[each]} is not equal {content[each]}"



    def test_field_availability(self):
        """
        Ensure that all mandantory field values are collected 
        """
        data_copy = self.data.copy()
        for key,value in self.data.items():
            data_copy.pop(key)

            response = self.client.put(self.url, data_copy, format='json')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            
            content = self.__correct_byte(response.content)       
            assert key in content, f'"{key}" should be a mandatory field in UserProfile model'
            # return the key value pair to the original dict
            data_copy[key]= value




    def test_password_validation(self):
        """
        Ensure that password validation works
        """
        data = self.data.copy()
        data["username"] = self.username
        data["password"] = "1234"

        response = self.client.put(self.url, data, format='json')
        content = self.__correct_byte(response.content)
        assert "password" in content, f" Incorrect password was authenticated"
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
       
