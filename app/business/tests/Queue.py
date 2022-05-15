from email.headerregistry import ContentTypeHeader
from django.test import Client
from django.urls import reverse
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

class BusinessQueueTests(APITestCase):
    def __init__(self, *args, **kwargs):
        super(BusinessQueueTests, self).__init__(*args, **kwargs)
                        
        self.queue_data =  {
            "name":"Coffee Queue",
            "information":"This queue is for cofffee",
            "instruction":"Please be availabe when it's your turn"
         }
        

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
        



    def test_create_queue(self):
        """
        Test create queue with valid parameters
        """
        new_data = self.queue_data.copy()
        response = self.client.post(reverse('business:queue_add'), new_data , format='json')
        content = self.__correct_byte(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # ensure equivalent values
        for key,value in new_data.items():
            self.assertEqual(str(value), str(content[key]))

   
    def test_update_queue_information(self):
        """
        Test update queue information
        """
        # create the queue
        response = self.client.post(reverse('business:queue_add'), self.queue_data , format='json')
        content = self.__correct_byte(response.content)
        pk = content.get('id')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


        

        # update queue info
        updated_data = {}
        updated_data['name'] = "Bread Queue"
        updated_data['information'] = "New Info"
        updated_data['instruction'] = "New Inst"
        response = self.client.patch(reverse('business:queue_info_update',kwargs={"pk":pk}),updated_data,format="json" )
        content = self.__correct_byte(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        for key,value in updated_data.items():
            self.assertEqual(str(value), str(content[key]))


    def test_view_queue_information(self):
        """
        Check the queue name,instruction and information
        """

        # create the queue
        response = self.client.post(reverse('business:queue_add'), self.queue_data , format='json')
        content = self.__correct_byte(response.content)
        pk = content.get('id')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


        # Create user profile account and
        # add user to the queue
        data =  DEFAULT_USER_PROFILE_DATA
        response = self.client.post(reverse('account:create_user_profile'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(username=data.get("username").lower())
        user.is_active = True
        user.save()
        userProfile = user.userProfile
        userProfile.current_business_queue = BusinessQueue.objects.get(pk=pk)
        userProfile.save()

        # check queue info
        response = self.client.get(reverse('business:queue_info_view',kwargs={"pk":pk}) )
        content = self.__correct_byte(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # check that it reflects num of people on the queue
        self.assertEqual(content.get("num_of_people"), 1,f"Queue information not reflecting the number of people current on the queue")


    def test_view_people_on_queue(self):
        """
        Check that it returns all users currently on the queue
        """
        # create the queue
        response = self.client.post(reverse('business:queue_add'), self.queue_data , format='json')
        content = self.__correct_byte(response.content)
        pk = content.get('id')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


        # Create user profile account and
        # add user to the queue
        data =  DEFAULT_USER_PROFILE_DATA
        response = self.client.post(reverse('account:create_user_profile'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(username=data.get("username").lower())
        user.is_active = True
        user.save()
        userProfile = user.userProfile
        userProfile.current_business_queue = BusinessQueue.objects.get(pk=pk)
        userProfile.save()

        # check queue info
        response = self.client.get(reverse('business:queue_view',kwargs={"pk":pk}) )
        content = self.__correct_byte(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # check that it reflects the user info of people on the queue
        self.assertEqual(content['people_on_queue'][0].get("user"), user.first_name)
        self.assertEqual(content['people_on_queue'][0].get("ticket"), userProfile.ticket)

    



    def test_delete_queue(self):
        """
        Test delete queue
        """
        # create the queue
        response = self.client.post(reverse('business:queue_add'), self.queue_data , format='json')
        content = self.__correct_byte(response.content)
        pk = content.get('id')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


        # Create user profile account and
        # add user to the queue
        data =  DEFAULT_USER_PROFILE_DATA
        response = self.client.post(reverse('account:create_user_profile'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(username=data.get("username").lower())
        user.is_active = True
        user.save()
        userProfile = user.userProfile
        userProfile.current_business_queue = BusinessQueue.objects.get(pk=pk)
        userProfile.save()

        # delete queue
        response = self.client.delete(reverse('business:queue_delete',kwargs={"pk":pk}) )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(BusinessQueue.objects.filter(pk=pk).exists(), False)
        

        # get updated userProfile object
        userProfile = User.objects.get(username=data.get("username").lower()).userProfile
        self.assertEqual(userProfile.current_business_queue, None)

    


    def test_athentication_permission(self):
        """
        Ensure that the user must be logged in order 
        to perform any of the actions relating to this test
        """

        c = Client() 
        response = c.get(reverse('business:queue_info_view',kwargs={'pk':1}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


        response = c.put(reverse('business:queue_info_update',kwargs={'pk':1}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = c.post(reverse('business:queue_add'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = c.post(reverse('business:queue_view',kwargs={'pk':1}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


        response = c.delete(reverse('business:queue_delete',kwargs={'pk':1}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


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

        response = c.get(reverse('business:queue_info_view',kwargs={'pk':1}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


        response = c.put(reverse('business:queue_info_update',kwargs={'pk':1}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = c.post(reverse('business:queue_add'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = c.post(reverse('business:queue_view',kwargs={'pk':1}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = c.delete(reverse('business:queue_delete',kwargs={'pk':1}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_is_business_owner_permission(self):
        """
        Ensure that the user is a owner of the account
        before any modification can be done
        """

        # Create first business profile account
        business_data =  DEFAULT_BUSINESS_PROFILE_DATA
        business_data["username"] = "starbucks_1"
        business_data["name"] = "starbucks_1"
        business_data["email"] = "starbucks_1@starbucks.com"
        response = self.client.post(reverse('account:create_business_profile'), business_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(username=business_data.get("username").lower())
        user.is_active = True
        user.save()


        # Create second business profile account
        business_data_2 =  DEFAULT_BUSINESS_PROFILE_DATA
        business_data_2["username"] = "starbucks_2"
        business_data_2["name"] = "starbucks_2"
        business_data_2["email"] = "starbucks_2@starbucks.com"
        response = self.client.post(reverse('account:create_business_profile'), business_data_2, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(username=business_data_2.get("username").lower())
        user.is_active = True
        user.save()

        # login first account
        c = Client() # authenticate new client object with user profile object
        c.login(username=business_data.get('username').lower(),
                password=business_data.get('password'))

        # create queue with first account
        new_queue_data = self.queue_data.copy()
        response = self.client.post(reverse('business:queue_add'), new_queue_data , format='json')
        content = self.__correct_byte(response.content)
        pk = content.get("id")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # login second account and try endpoints with it
        c2 = Client() # authenticate new client object with user profile object
        c2.login(username=business_data_2.get('username').lower(),
                password=business_data_2.get('password'))

        response = c2.get(reverse('business:queue_info_view',kwargs={'pk':pk}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


        response = c2.put(reverse('business:queue_info_update',kwargs={'pk':pk}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = c2.get(reverse('business:queue_view',kwargs={'pk':pk}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = c2.delete(reverse('business:queue_delete',kwargs={'pk':pk}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


