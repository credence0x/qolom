from urllib import request
from rest_framework import serializers
from account.models import UserProfile
from django.contrib.auth import get_user_model
from account.module.generate_random import getRandomTicket
from account.module.variables import SPECIAL_CHARS
from core.module.email import Email
from account.serializers.user import UserSerializer,UpdateUserSerializer

User = get_user_model()

user_profile_editable_fields = (
                                "country",
                                "iso_code",
                                "first_name",
                                "last_name",
                                "password",
                                "user",
                                )

user_profile_base_fields =  (
                            "username",
                            "d_o_b",
                            "password_2",
                            "email",
                            "ticket",
                            ) + user_profile_editable_fields 




class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
  
    class Meta:
        model = UserProfile
        fields = user_profile_base_fields



class CreateUserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)
    first_name = serializers.CharField(write_only=True)
    last_name = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    password_2 = serializers.CharField(write_only=True)
    ticket = serializers.CharField(read_only=True)
    user = UserSerializer(read_only=True)


    
    class Meta:
        model = UserProfile
        fields = user_profile_base_fields

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
        password_1, password_2 = data.get('password'), data.get('password_2')
        if password_1 != password_2:
            raise serializers.ValidationError({"password":"Passwords did not match"})
        return data

        
    def create(self,validated_data):    
        ticket = getRandomTicket(6)
        user = User.objects.create_user(username=validated_data.get('username'),
                                        password=validated_data.get('password'),
                                        first_name=validated_data.get('first_name'),
                                        last_name=validated_data.get('last_name'),
                                        email = validated_data.get('email'),
                                        is_active=False
                                        )
        
        userProfile = UserProfile.objects.create( user=user,
                                    ticket = ticket,
                                    country=validated_data.get('country'),
                                    iso_code=validated_data.get('iso_code'),
                                    d_o_b=validated_data.get('d_o_b'),  
                                    total_seconds=0
                                )
        return userProfile










class UpdateUserProfileSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField(write_only=True,required=False)
    last_name = serializers.CharField(write_only=True,required=False)
    user = UpdateUserSerializer(read_only=True)

    
    class Meta:
        model = UserProfile
        fields = user_profile_editable_fields



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

                
        


       