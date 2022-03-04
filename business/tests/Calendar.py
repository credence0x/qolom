from django.test import Client
from django.urls import reverse
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

class CalendarTests(APITestCase):
    def __init__(self, *args, **kwargs):
        super(CalendarTests, self).__init__(*args, **kwargs)
                        
        self.calendar_data =  { }
        for day in variables.LIST_OF_DAYS:
            open_time = f"{day}_o"
            closing_time = f"{day}_c"
            self.calendar_data[open_time] = datetime.time(13,10,50) # 1:10 PM
            self.calendar_data[closing_time] = datetime.time(23,59,59) # 11:59 PM


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
        cls.data = create_data
        cls.username = user.username
        cls.password = create_data.get("password")
        
    
    def setUp(self):
        self.client.login(username=self.username.lower(),
                            password=self.password)
        



    def test_view_calendar(self):
        response = self.client.get(reverse('business:calendar_view'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)





    def test_update_calendar(self):
        """
        Test update calendar with valid parameters
        """
        updated_data = self.calendar_data.copy()
        response = self.client.patch(reverse('business:calendar_update'), updated_data , format='json')
        content = self.__correct_byte(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # ensure equivalent values
        for key,value in updated_data.items():
            self.assertEqual(str(value), str(content[key]))


    def test_update_calendar_with_overlapping_dates(self):
        """
        Test update calendar with overlapping parameters
        """
        updated_data = self.calendar_data.copy()
        updated_data["mo_o"] = datetime.time(4,0,0)
        updated_data["mo_c"] = datetime.time(2,0,0)
        response = self.client.patch(reverse('business:calendar_update'), updated_data , format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)




    def test_update_calendar_with_single_null_value(self):
        """
        Test update calendar with single null value
        """
        updated_data = self.calendar_data.copy()
        updated_data["mo_c"] = None
        response = self.client.patch(reverse('business:calendar_update'), updated_data , format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    
    def test_update_calendar_with_double_null_value(self):
        """
        Test update calendar with double null value
        """
        updated_data = self.calendar_data.copy()
        updated_data["mo_o"] = None
        updated_data["mo_c"] = None
        response = self.client.patch(reverse('business:calendar_update'), updated_data , format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_athentication_permission(self):
        """
        Ensure that the user must be logged in order 
        to perform any of the actions relating to this test
        """

        c = Client() 
        response = c.post(reverse('business:calendar_update'), self.calendar_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


        response_2 = c.post(reverse('business:calendar_view'), self.calendar_data, format='json')
        self.assertEqual(response_2.status_code, status.HTTP_403_FORBIDDEN)



    def test_is_business_permission(self):
        """
        Ensure that the user is a business account
        """

        # Create user profile account
        data =  DEFAULT_USER_PROFILE_DATA
        response = self.client.post(reverse('account:create_user_profile'), data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(username=data.get("username").lower())
        user.is_active = True
        user.save()

        # actual test
        c = Client() # authenticate new client object with user profile object
        c.login(username=data.get('username').lower(),
                password=data.get('password'))

        response = c.post(reverse('business:calendar_update'), self.calendar_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response_2 = c.post(reverse('business:calendar_view'), self.calendar_data, format='json')
        self.assertEqual(response_2.status_code, status.HTTP_403_FORBIDDEN)


