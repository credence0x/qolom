from email.headerregistry import ContentTypeHeader
from operator import concat
from turtle import update
from django.test import Client
from django.urls import reverse
from business.models.Order import Item, Order, PurchasedItem
from business.models.Queue import BusinessQueue
from rest_framework import status
from rest_framework.test import APITestCase
import datetime
from django.contrib.auth import get_user_model
from business.module import variables
import json

User = get_user_model()

DEFAULT_CARD_DATA = {
                    'authorization_code': 'AUTH_cp37r9l8hy',
                    'bin': '408408', 
                    'last4': '4081',
                    'exp_month': '12', 
                    'exp_year': '2030', 
                    'brand': 'visa', 
                    'signature': 'SIG_wtJnxFyk01mwpXCQAh6e',
                    'account_name': "Test Account Name",
                }

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




class CardTests(APITestCase):
    def __init__(self, *args, **kwargs):
        super(CardTests, self).__init__(*args, **kwargs)
                        
        
        

    def __correct_byte(self,byte_value):
        return json.loads(byte_value.decode('utf-8'))
    
    @classmethod    
    def setUpTestData(cls):

        # create end user
        create_data = DEFAULT_USER_PROFILE_DATA.copy()
        

        url = reverse('account:create_user_profile')
        c = Client()
        c.post(url, create_data, format='json')
        user = User.objects.get(username=create_data.get("username").lower())
        user.is_active = True
        user.save()
        cls.user = user
        cls.username = user.username
        cls.password = create_data.get("password")


        # create card
        c.login(username=user.username.lower(),
                            password=create_data.get("password"))

        card_data = DEFAULT_CARD_DATA.copy()
        response = c.post(reverse('users:card_create_or_list'),card_data,format="json")
        content = json.loads(response.content.decode('utf-8'))
        cls.default_card_id = content.get("id")   
        assert response.status_code == status.HTTP_201_CREATED


      
    
    def setUp(self):
        self.client.login(username=self.username.lower(),
                            password=self.password)
        


    def test_add_card(self):
        """
        Ensure you can add a card object
        """
        data = DEFAULT_CARD_DATA.copy()
        response = self.client.post(reverse('users:card_create_or_list'),data,format="json")
        content = self.__correct_byte(response.content)  
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        for k,v in data.items():
            self.assertEqual(str(v),str(content.get(k)))

    def test_list_cards(self):
        """
        Ensure you can find all card objects
        """
        response = self.client.get(reverse('users:card_create_or_list'))

        content = self.__correct_byte(response.content)  
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_card(self):
        """
        Ensure you can retrieve card
        """
        response = self.client.get(reverse('users:card_retrieve_update_or_delete',args=[self.default_card_id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_card(self):
        """
        Ensure you can update card
        """
        data = {"bin":"456789"}
        response = self.client.put(reverse('users:card_retrieve_update_or_delete',args=[self.default_card_id]),data,format="json")
        content = self.__correct_byte(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(content.get("bin"), data.get("bin"))
        

    def test_delete_card(self):
        """
        Ensure you can delete card
        """
        response = self.client.delete(reverse('users:card_retrieve_update_or_delete',args=[self.default_card_id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
