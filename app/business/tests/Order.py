from email.headerregistry import ContentTypeHeader
from turtle import update
from django.test import Client
from django.urls import reverse
from account.models.UserProfile import CardInformation
from business.models.Order import Item, Order
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
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        


    def test_delete_item(self):
        """
        Ensure you can delete item 
        """
        response = self.client.delete(reverse('business:item_delete',args=[self.default_item.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        










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






class BusinessOrderTests(APITestCase):
    def __init__(self, *args, **kwargs):
        super(BusinessOrderTests, self).__init__(*args, **kwargs)
                        
        
        

    def __correct_byte(self,byte_value):
        return json.loads(byte_value.decode('utf-8'))
    
    @classmethod    
    def setUpTestData(cls):

        # create end user
        create_data = DEFAULT_USER_PROFILE_DATA
        

        url = reverse('account:create_user_profile')
        c = Client()
        c.post(url, create_data, format='json')
        user = User.objects.get(username=create_data.get("username").lower())
        user.is_active = True
        user.save()
        cls.user = user
        cls.username = user.username
        cls.password = create_data.get("password")


        # Create Business
        business_create_data = DEFAULT_BUSINESS_PROFILE_DATA

        url = reverse('account:create_business_profile')
        bc = Client()
        bc.post(url, business_create_data, format='json')
        business_user = User.objects.get(username=business_create_data.get("username").lower())
        business_user.is_active = True
        business_user.save()
        cls.business_user = business_user
        cls.business_username = business_user.username
        cls.business_password = business_create_data.get("password")


        # login business account

        bc.login(username=business_user.username,
        password=business_create_data.get("password")
        )

        # create item 1

        item_data = DEFAULT_ITEM_DATA.copy()
        item_data["name"] = "Item 1"
        response = bc.post(reverse('business:item_add'),item_data,format="json")
        content = json.loads(response.content.decode('utf-8'))
        assert response.status_code == status.HTTP_201_CREATED
        item_1 = Item.objects.get(id=content.get("id"))
        cls.item_1 = item_1

        # create item 2
        
        item_data_2 = DEFAULT_ITEM_DATA.copy()
        item_data_2["name"] = "Item 2"
        response = bc.post(reverse('business:item_add'),item_data_2,format="json")
        content = json.loads(response.content.decode('utf-8'))
        assert response.status_code == status.HTTP_201_CREATED
        
        cls.item_2 = Item.objects.get(id=content.get("id"))
        

       
    
    

   
     


    def test_list_order(self):
        """
        Ensure you can list orders
        """
        # create order using userProfile account
        self.client.login(username=self.username.lower(),
                            password=self.password)
        data = {
            "seller":self.business_user.businessProfile.id,
            "items":[
                {
                    "id":self.item_1.id,
                    "units":"4",
                },
                {
                    "id":self.item_2.id,
                    "units":"7",
                }
            ]
        }
        response = self.client.post(reverse('users:order_add'),data,format="json")
        content = self.__correct_byte(response.content)      
        order_id_1 = content.get("id") 
        order_1 = Order.objects.get(id=order_id_1)
        order_1.status = 2
        order_1.save()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # create order 2
        response = self.client.post(reverse('users:order_add'),data,format="json")
        content = self.__correct_byte(response.content)      
        order_id_2 = content.get("id") 
        order_2 = Order.objects.get(id=order_id_2)
        order_2.status = 2
        order_2.save()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


        # create order 3
        response = self.client.post(reverse('users:order_add'),data,format="json")
        content = self.__correct_byte(response.content)      
        # Note that the status isn't changed from it's 
        # default value of 1
        # this is to ensure that it doesn't show 
        # orders with status < 2
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # list orders
        self.client.login(username=self.business_username.lower(),
                            password=self.business_password)
        response = self.client.get(reverse('business:order_list'))
        content = self.__correct_byte(response.content)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(content) == 2, True)
        for each in content:
            assert each.get("status") >= 2








    def test_update_order_status(self):
        """
        Ensure you can update order status to either 
        3 ("READY") or 4 ("COLLECTED")
        """
        # create order using userProfile account
        self.client.login(username=self.username.lower(),
                            password=self.password)
        data = {
            "seller":self.business_user.businessProfile.id,
            "items":[
                {
                    "id":self.item_1.id,
                    "units":"4",
                },
                {
                    "id":self.item_2.id,
                    "units":"7",
                }
            ]
        }
        response = self.client.post(reverse('users:order_add'),data,format="json")
        content = self.__correct_byte(response.content)      
        order_id_1 = content.get("id") 
        order_1 = Order.objects.get(id=order_id_1)
        order_1.status = 2
        order_1.save()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # create order 2
        response = self.client.post(reverse('users:order_add'),data,format="json")
        content = self.__correct_byte(response.content)      
        order_id_2 = content.get("id") 
        order_2 = Order.objects.get(id=order_id_2)
        order_2.status = 3
        order_2.save()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


        # test update to 4 ("COLLECTED") when the current
        # order status == 2 (for Order 1)
        # This will result in an error stating
        # that the wrong status was inputed
        self.client.login(username=self.business_username.lower(),
                            password=self.business_password)
        update_data = {
            "status":4,
        }

       
        response = self.client.patch(reverse('business:order_update_status',args=[order_id_1]),update_data,format="json")
        error = self.__correct_byte(response.content)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("status",error)



        # input appropriate order status (i.e 4) for Order 2
        update_data["status"] = 4
        update_data["pin"] = order_2.pin
        
        response = self.client.patch(reverse('business:order_update_status',args=[order_id_2]),update_data,format="json")
        content = self.__correct_byte(response.content)   
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(content.get("status"), update_data.get("status"))



        # input appropriate order status (i.e 3) for Order 1
        update_data["status"] = 3
        del update_data["pin"]
        response = self.client.patch(reverse('business:order_update_status',args=[order_id_1]),update_data,format="json")
        content = self.__correct_byte(response.content)   
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(content.get("status"), update_data.get("status"))