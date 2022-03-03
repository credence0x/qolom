from rest_framework import serializers 
from django.contrib.auth import get_user_model
from django.contrib.auth import login,logout
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_text
from account.module.businessProfile.serializers.utils import ensure_user_has_related_business_profile_object
from account.module.email import Email
from account.tokens import account_activation_token

User = get_user_model()


class ActivateBusinessProfileTokenSerializer(serializers.Serializer):
    """
    Confirm account activation url
    """
    uidb64 = serializers.CharField(write_only=True)
    token = serializers.CharField(write_only=True)
    class Meta:
        fields = ("uidb64","token")

    def validate(self,data):
        # confirm uidb64
        uidb64 = data.get("uidb64")
        token = data.get("token")

        try:
            user_id = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)
            data["user"] = user
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise serializers.ValidationError({"Invalid Token"})
        
        # ensures that it is a business account
        ensure_user_has_related_business_profile_object(user)

        # confirm token
        if not account_activation_token.check_token(user, token):
            raise serializers.ValidationError({"Invalid Token"})
            
        return data


    def save(self):
        request = self.context.get("request")
        user = self.validated_data.get("user")
        if not user.is_active:
            user.is_active = True
            user.save()
            Email(request,user).send_common_welcome_mail()




class AuthenticateBusinessProfileSerializer(serializers.Serializer):
    """" 
    Log In 
    """
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


    class Meta:
        fields = ("username","password")

    def validate_username(self,value):
        value = value.lower()
        return value
        
    def validate(self,data):
        request = self.context.get("request")
        username, password = data.get('username'), data.get('password')
        user_data = {"username":username} if "@" not in username else {"email":username}
        try:    
            user = User.objects.get(**user_data)
        except User.DoesNotExist:
            raise serializers.ValidationError({"username":"Username and password did not match"})

        # ensures that it is a business account
        ensure_user_has_related_business_profile_object(user)
        

        correct_password = user.check_password(password) 
        if not correct_password:
            raise serializers.ValidationError({"username":"Username and password did not match"})

        if user.is_active and correct_password:
            login(request, user)
        elif correct_password and (not user.is_active):
            raise serializers.ValidationError({"account":"Please activate your account"})   
        return data

    def save(self):
        validated_data = self.validated_data
        username = validated_data.get('username')
        user_data = {"username":username} if "@" not in username else {"email":username}
        user = User.objects.get(**user_data)
        businessProfile = user.businessProfile
        return businessProfile
    
   
 


class DeauthenticateBusinessProfileSerializer(serializers.Serializer):
    """ 
    Log Out
    """
    def save(self):
        request = self.context.get("request")
        logout(request)
   
 

