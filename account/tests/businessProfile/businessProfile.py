import os
from django.test import Client
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
import datetime,json
from PIL import Image

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings


User = get_user_model()



class CreateBusinessProfileTests(APITestCase):
    def __init__(self, *args, **kwargs):
        super(CreateBusinessProfileTests, self).__init__(*args, **kwargs)
        
        self.data =  {    
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

        self.url = reverse('account:create_business_profile')

    
    def __correct_byte(self,byte_value):
        return json.loads(byte_value.decode('utf-8'))
        
   
   

    def test_create_business_profile(self):
        """
        Ensure we can create a new business profile object.
        """
        data = self.data.copy()
        response = self.client.post(self.url, data, format='json')
        content = self.__correct_byte(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # make sure the key exists and its length is 7 
        self.assertEqual(len(content.get("key")), 7)

        user_field_list = [
                            "username",
                            "email",
                            ]
        for each in user_field_list:
            # assert that the correct values were actually inserted
            self.assertEqual(data[each].lower(),
                            content['user'][each].lower(),
                             f"{data[each]} is not equal {content['user'][each]}"
                            )

        user = User.objects.get(username=self.data['username'].lower())
        correct_password = user.check_password(self.data["password"])
        self.assertEqual(correct_password,
                            True,
                            "The inputed password is not the same as the saved password"
                            )
        
        
        BusinessProfile_field_list = [
                            "name",
                            "country",
                            "state",
                            "address",
                            "minimum_age_allowed",
                            "iso_code",
                        ]

        for each in BusinessProfile_field_list:
            # assert that the correct values were actually inserted 
            self.assertEqual(
                                str(data[each]),
                                str(content[each]),
                                f"{data[each]} is not equal {content[each]}"
                            )           
            


        

    



    def test_field_availability(self):
        """
        Ensure that all mandantory field values are collected 
        """
        data = self.data.copy()
        data_copy = self.data.copy()

        # remove non compulsory fiels
        non_compulsory_fields = ["minimum_age_allowed"]
        for i in non_compulsory_fields:
            del data_copy[i]
            del data[i]

        for key,value in data.items():
            
            data_copy.pop(key)

            response = self.client.post(self.url, data_copy, format='json')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            
            content = self.__correct_byte(response.content)       
            self.assertIn( key, content, f'"{key}" should be a mandatory field in BusinessProfile model')
            # return the key value pair to the original dict
            data_copy[key]= value




    def test_validation(self):
        """
        Ensure that all field validations work
        """
        data = self.data.copy()
        data["username"] = "lanre"
        data["password"] = "1234"

        # username and password validation

        # check number of characters
        response = self.client.post(self.url, data, format='json')
        error = self.__correct_byte(response.content)
        self.assertIn("username",error, f' Username should have up to 6 characters')
        self.assertIn("password",error, f' Passwords must have up to 8 characters and a special character')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        

        # check "@" symbol

        data["username"] = "testbusiness@businessname.com"
        data["password"] = self.data.get("password")

        response = self.client.post(self.url, data, format='json')
        error = self.__correct_byte(response.content)
        self.assertIn("@",
            error["username"][0], 
            f"Username must not contain the '@' symbol"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        

        # check mismatched passwords

        data["username"] = self.data.get("username")
        data["password"] = self.data.get("password")
        data["password_2"] = "different_from_first_password"

        response = self.client.post(self.url, data, format='json')
        content = self.__correct_byte(response.content)
        self.assertEqual(content["password"][0], 'Passwords did not match')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)



















class UpdateAndListBusinessProfileTests(APITestCase):
    def __init__(self, *args, **kwargs):
        super(UpdateAndListBusinessProfileTests, self).__init__(*args, **kwargs)
                        
        self.data =  {      "name":"Starbucks Local Ltd",
                            "password":"1234@334&*9",
                            "iso_code":"NG",
                            "country":"Ukraine",
                            "state":"Kyiv",
                            "address":"The Presidential Villa",
                     }
        
    
    def __correct_byte(self,byte_value):
        return json.loads(byte_value.decode('utf-8'))
    
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
            }
        

        url = reverse('account:create_business_profile')
        c = Client()
        c.post(url, create_data, format='json')
        user = User.objects.get(username=create_data.get("username").lower())
        user.is_active = True
        user.save()
        cls.username = user.username
        cls.password = create_data.get("password")
        cls.url = reverse('account:update_business_profile',kwargs={'pk': user.businessProfile.pk})

    
    def setUp(self):
        self.client.login(username=self.username.lower(),
                            password=self.password)
        



    def test_authentication(self):
        """
        Ensure that the user must be logged in order 
        to perform any of the actions relating to this test
        """
        data = self.data.copy()
        c = Client() # and not self.client which is already logged in
        response = c.put(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
   
   
        
    
    def test_update_business_profile(self):
        """
        Ensure we can update business profile object.
        """
        data = self.data.copy()
        profile_pic_path = os.path.join(settings.BASE_DIR,"test_files","bored_ape.jpg")
        with open(profile_pic_path,"rb") as picture_data:
            data["profile_picture"] = picture_data            
            response = self.client.put(self.url, data, format='multipart')
            content = self.__correct_byte(response.content)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            
            BusinessProfile_field_list = self.data.keys()
            exempt = ["password"]
            for each in BusinessProfile_field_list:
                if each not in exempt:
                    # assert that the correct values were actually inserted            
                    self.assertEqual(str(data[each]),content[each], f"{data[each]} is not equal {content[each]}")



   

    def test_password_validation(self):
        """
        Ensure that the business has to enter the correct password in 
        order to change profile data
        """
        data = self.data.copy()
        data["username"] = self.username
        data["password"] = "1234"

        response = self.client.put(self.url, data, format='json')
        content = self.__correct_byte(response.content)
        self.assertIn("password", content, f" Incorrect password was authenticated")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    
    
    
    def test_business_list(self):
        """
        Ensure that you can find a businesses
        """
        

        response = self.client.get(reverse("account:list_business_profile"))
        content = self.__correct_byte(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(content), 1)
        