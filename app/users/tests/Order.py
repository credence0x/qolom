from email.headerregistry import ContentTypeHeader
from operator import itemgetter
from turtle import update
from django.test import Client
from django.urls import reverse
from account.models.UserProfile import CardInformation
from business.models.Order import Item, Order, PurchasedItem
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

class UserOrderTests(APITestCase):
    def __init__(self, *args, **kwargs):
        super(UserOrderTests, self).__init__(*args, **kwargs)
                        
        
        

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
        

        # create card
        c.login(username=user.username.lower(),
                            password=create_data.get("password"))

        card_data = DEFAULT_CARD_DATA.copy()
        response = c.post(reverse('users:card_create_or_list'),card_data,format="json")
        content = json.loads(response.content.decode('utf-8'))
        cls.default_card = CardInformation.objects.get(id=content.get("id"))   
        assert response.status_code == status.HTTP_201_CREATED
    
    def setUp(self):
        self.client.login(username=self.username.lower(),
                            password=self.password)
        


    def test_create_order(self):
        """
        Ensure you can create an order
        """
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
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_order_with_invalid_quantity(self):
        """
        Ensure you can't create an order
        where quantity requested is greater
        than quantity available

        Also ensure that only positive numbers 
        are accepted
        """
        # test for negative number
        data =  {
            "seller":self.business_user.businessProfile.id,
            "items":[
                {
                    "id":self.item_1.id,
                    "units":"-1",
                },
            ]
        }
        response = self.client.post(reverse('users:order_add'),data,format="json")

        content = self.__correct_byte(response.content)  
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("items", content)



        # test for quantity greater than available
        data["items"][0]["units"] = "7777777777777"

        response = self.client.post(reverse('users:order_add'),data,format="json")
        content = self.__correct_byte(response.content)  
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("items", content)


    

    def test_initialize_order(self):
        """
        Ensure order initialization works
        and get link for final payment
        """
        # create order
        data = {
            "seller":self.business_user.businessProfile.id,
            "items":[
                {
                    "id":self.item_1.id,
                    "units":"12",
                },
            ]
        }
        response = self.client.post(reverse('users:order_add'),data,format="json")
        content = self.__correct_byte(response.content)  
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        order_id = content.get("id")



        # initialize order
        init_data = {"id":order_id}
        response = self.client.post(reverse('users:order_initialize'),init_data,format="json")
        content = self.__correct_byte(response.content)  
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("authorization_url",content["data"])
       
    





    

    def test_verify_order(self):
        """
        Ensure verify order
        """
        # create order
        data = {
            "seller":self.business_user.businessProfile.id,
            "items":[
                {
                    "id":self.item_1.id,
                    "units":"12",
                },
            ]
        }

        response = self.client.post(reverse('users:order_add'),data,format="json")
        content = self.__correct_byte(response.content)  
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        order_id = content.get("id")



        # initialize order
        init_data = {"id":order_id}
        response = self.client.post(reverse('users:order_initialize'),init_data,format="json")
        content = self.__correct_byte(response.content)  
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("authorization_url",content["data"])
       

        # Verify only initialized but unpaid order

        # order was only initialized so it
        # should return False since it has not
        # been paid for
        
        reference_dict = {"reference":content["data"].get("reference")}
        response = self.client.post(reverse('users:order_verify'),reference_dict,format="json")
        content = self.__correct_byte(response.content)  
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(content.get("success"),False)




        # Verify paid order

        # change order reference to a 
        # confirmed ref since I can't charge 
        # the order manually
        verified_reference = "dnbpa2yd1b"
        order = Order.objects.get(id=order_id) 
        order.reference = verified_reference
        order.save()
        verified_reference_dict = {"reference":verified_reference}
        response = self.client.post(reverse('users:order_verify'),verified_reference_dict,format="json")
        content = self.__correct_byte(response.content)  
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(content.get("success"),True)






    def test_pay_with_saved_card(self):
        """
        Ensure payment with saved card works
        """
        # create order
        data = {
            "seller":self.business_user.businessProfile.id,
            "items":[
                {
                    "id":self.item_1.id,
                    "units":"12",
                },
            ]
        }
        response = self.client.post(reverse('users:order_add'),data,format="json")
        content = self.__correct_byte(response.content)  
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        order_id = content.get("id")


        # actual test
        data = {
            "id":order_id,
            "last4":self.default_card.last4,
        }
        response = self.client.post(reverse('users:order_pay_with_card'),data,format="json")
        content = self.__correct_byte(response.content)  
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        

    def test_list_orders(self):
        """
        Ensure user can find all orders created
        """
        # create order 1
        data = {
            "seller":self.business_user.businessProfile.id,
            "items":[
                {
                    "id":self.item_1.id,
                    "units":"12",
                },
            ]
        }

        response = self.client.post(reverse('users:order_add'),data,format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # create order 2
        response = self.client.post(reverse('users:order_add'),data,format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        


        # list orders
        response = self.client.get(reverse('users:order_list'))
        content = self.__correct_byte(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(content) > 1, True)