from account.module.businessProfile.serializers.utils import compress_image
from business.models.Calendar import Calendar
from rest_framework import serializers
from account.models import BusinessProfile
from django.contrib.auth import get_user_model
from account.module.generate_random import getRandomTicket
from account.module.variables import SPECIAL_CHARS
from account.serializers.user import UserSerializer, UpdateUserSerializer
from business.module import variables
import datetime


User = get_user_model()

business_profile_editable_fields = (
                                    "password",
                                    "country",
                                    "state",
                                    "address",
                                    "iso_code",     
                                    "name",
                                    "minimum_age_allowed",
                                    "profile_picture",
                                    "user", # read_only=True
                                )

business_profile_base_fields =  (
                                "username",
                                "email",
                                "key",

                              ) + business_profile_editable_fields 


    

    




class BusinessProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
  
    class Meta:
        model = BusinessProfile
        fields = business_profile_base_fields



class CreateBusinessProfileSerializer(serializers.ModelSerializer):
    profile_picture = serializers.FileField(required=False,
                                            write_only=True)
    username = serializers.CharField(write_only=True)
    key = serializers.CharField(required=False)
    email = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    password_2 = serializers.CharField(write_only=True)
    user = UserSerializer(read_only=True)
    


    
    class Meta:
        model = BusinessProfile
        fields = business_profile_base_fields + ("password_2",)
    
    
    def validate_profile_picture(self,value):
        return compress_image(value)


    def validate_email(self,value):
        value = value.lower()
        user = User.objects.filter(email=value).exists()
        if user:
            raise serializers.ValidationError('This e-mail address is already registered to another account')
        return value

    


    def validate_username(self,value):
        value = value.lower()
        if len(value) < 6:
            raise serializers.ValidationError("Username must contain up to 6 characters")
        if ' ' in value:
            raise serializers.ValidationError("A blank space can not be included as part of your username")
        if '@' in value:
            raise serializers.ValidationError("@ symbol can not be included as part of your username")
        user = User.objects.filter(username=value).exists()
        if user:
            raise serializers.ValidationError('Username is already taken. Please choose another username')
        return value



    def validate_password(self,value):
        if len(value) < 8:
            raise serializers.ValidationError("Password must contain up to 8 characters including a number or special character")
        
        contains_special_char = False
        for at_least_one in SPECIAL_CHARS:
            if at_least_one in value:
                contains_special_char = True
                break
        if not contains_special_char:
            raise serializers.ValidationError("Password must contain a number or special character")
        
        return value



    def validate(self,data):
        business_name = data.get("name")
        password_1, password_2 = data.get('password'), data.get('password_2')
        if password_1 != password_2:
            raise serializers.ValidationError({"password":"Passwords did not match"})
        business_exists = BusinessProfile.objects.filter(name__iexact=business_name,iso_code=data.get('iso_code')).exists()
        if business_exists:
            raise serializers.ValidationError({"name": f"A business with the name '{business_name}' already exists in your country."})
        return data

        
    def create(self,validated_data):    
        key = getRandomTicket(7)
        user = User.objects.create_user(
                                username=validated_data.get('username'),
                                password=validated_data.get('password'),
                                email = validated_data.get('email'),
                                is_active=False
                            )
        
        businessProfile = BusinessProfile.objects.create( 
                                    user=user,
                                    key= key,
                                    country=validated_data.get('country'),
                                    state=validated_data.get('state'),
                                    address=validated_data.get('address'),
                                    iso_code=validated_data.get('iso_code'),
                                    name=validated_data.get('name'),  
                                    minimum_age_allowed=validated_data.get('minimum_age_allowed'),  
                                    profile_picture=validated_data.get('profile_picture'),  
                                )

        # initalize Calendar
        calendar_data =  {"owner":businessProfile}
        Calendar.objects.create(**calendar_data)


        return businessProfile










class UpdateBusinessProfileSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True) # required
    name = serializers.CharField(required=False)
    address = serializers.CharField(required=False)
    country = serializers.CharField(required=False)
    state = serializers.CharField(required=False)
    iso_code = serializers.CharField(required=False)
    profile_picture = serializers.ImageField(required=False)

    # essentially does nothing since first_name and last_name can't be updated
    user = UpdateUserSerializer(write_only=True,required=False)

    
    class Meta:
        model = BusinessProfile
        fields = business_profile_editable_fields


    def validate_profile_picture(self,value):
        return compress_image(value)


    def validate_password(self,value):
        request = self.context.get("request")
        user = request.user
        if not user.check_password(value):
            raise serializers.ValidationError("Invalid Password")
        return value


    def update(self,instance,validated_data):
        for key,value in validated_data.items():
            setattr(instance,key,value)
        user = instance.user
        user.first_name = validated_data.get("first_name",user.first_name)
        user.last_name = validated_data.get("last_name",user.last_name)
        user.save()
        instance.save()
        return instance

                
        


       