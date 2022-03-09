from email.headerregistry import ContentTypeHeader
from turtle import update
from django.test import Client
from django.urls import reverse
from business.models.Order import Item
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

DEFAULT_ITEM_DATA = {    
                                    "name": "Coffee",
                                    "price":"2000",
                                    "units":"20"
                                }

class ItemTests(APITestCase):
    def __init__(self, *args, **kwargs):
        super(ItemTests, self).__init__(*args, **kwargs)
                        
        
        

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

        # create initial item

        c.login(username=user.username,
        password=create_data.get("password")
        )
        item_data = DEFAULT_ITEM_DATA.copy()
        item_data["name"] = "Initial Item"
        response = c.post(reverse('business:item_add'),item_data,format="json")
        content = json.loads(response.content.decode('utf-8'))
        assert response.status_code == status.HTTP_201_CREATED
        cls.default_item = Item.objects.get(id=content.get("id"))
        
    
    def setUp(self):
        self.client.login(username=self.username.lower(),
                            password=self.password)
        


    def test_create_item(self):
        """
        Ensure you can create an item that can be ordered
        """
        data = DEFAULT_ITEM_DATA
        response = self.client.post(reverse('business:item_add'),data,format="json")
        
        content = self.__correct_byte(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
       
    def test_double_create_item(self):
        """
        Ensure you can't create two 
        items with the same name
        """
        data = DEFAULT_ITEM_DATA.copy()
        # first time
        response = self.client.post(reverse('business:item_add'),data,format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        #second_time
        response = self.client.post(reverse('business:item_add'),data,format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_item(self):
        """
        Ensure you can't get all items
        related to a business
        """
        # get list
        response = self.client.get(reverse('business:item_list'))
        content = self.__correct_byte(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_update_item(self):
        """
        Ensure you can't update item data
        """
        updated_data = {
            "name":"Coffee 1",
            "units":"70",
            "price":"1000"
        }
        response = self.client.put(reverse('business:item_update',args=[self.default_item.id]),updated_data,format="json")
        content = self.__correct_byte(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for k,v in updated_data.items():
            self.assertEqual(str(v),str(content.get(k)))


    def test_retrieve_item(self):
        """
        Ensure you can retrieve item data
        """
        response = self.client.get(reverse('business:item_retrieve',args=[self.default_item.id]))
        content = self.__correct_byte(response.content)
        print(content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        


    def test_delete_item(self):
        """
        Ensure you can delete item 
        """
        response = self.client.delete(reverse('business:item_delete',args=[self.default_item.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        


