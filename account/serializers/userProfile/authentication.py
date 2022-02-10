from rest_framework import serializers 
from django.contrib.auth.models import User
from django.contrib.auth import login,logout



class AuthenticateUserSerializer(serializers.Serializer):
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
            bool(user.userProfile)
            # both lines above are equally important
        except User.DoesNotExist:
            raise serializers.ValidationError({"username":"Username and password did not match"})
        
        
        correct_password = user.check_password(password) 
        if not correct_password:
            raise serializers.ValidationError({"username":"Username and password did not match"})

        elif user.is_active and correct_password:
            login(request, user)
            

        elif correct_password and (not user.is_active):
            raise serializers.ValidationError({"account":"Please activate your account"})   
        return data

    def save(self):
        validated_data = self.validated_data
        username = validated_data.get('username')
        user_data = {"username":username} if "@" not in username else {"email":username}
        user = User.objects.get(**user_data)
        userProfile = user.userProfile
        return userProfile
    
   
 


class DeauthenticateUserSerializer(serializers.Serializer):
    def save(self):
        request = self.context.get("request")
        logout(request)
   
 

