from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.utils.encoding import force_text
from account.tokens import account_activation_token_three
from django.utils.http import urlsafe_base64_decode
from account.module.variables import SPECIAL_CHARS

User = get_user_model()

class ResetPasswordSerializer(serializers.Serializer):
    uidb64 = serializers.CharField(write_only=True)
    token = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    password_2 = serializers.CharField(write_only=True)

    class Meta:
        fields = ("uidb64","token","password","password_2")


         

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

        uidb64 = data.get("uidb64")
        token = data.get("token")

        #uidb64
        try:
            user_id = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise serializers.ValidationError("Invalid Token")


        #tokens
        if not account_activation_token_three.check_token(user, token):
            raise serializers.ValidationError("Invalid Token")

        # compare passwords
        password,password_2 = data.get("password"),data.get("password_2")
        if password != password_2:
            raise serializers.ValidationError({"password":"Passwords did not match"})
        data["user"]= user
        return data

    def save(self):
        user = self.validated_data.get("user")
        user.set_password(self.validated_data.get('password'))
        user.save()
    
        


    
    
        