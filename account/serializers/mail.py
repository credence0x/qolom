from dataclasses import field
from rest_framework import serializers
from account.module.email import Email
from django.contrib.auth import get_user_model
from account.module.utils import get_asterisked_mail
from django.contrib.sites.shortcuts import get_current_site


User = get_user_model()


class SignUpMailSerializer(serializers.Serializer):
    username = serializers.CharField(write_only=True)
    uidb64 = serializers.CharField(read_only=True,required=False)
    token = serializers.CharField(read_only=True,required=False)

    class Meta:
        fields = ("username","uidb64","token")

    def validate(self,data):
        """ 
        Make sure that User account exists and the user is active
        """
        username = data.get('username')
        username = username.lower()
        user_data = {"username":username} if "@" not in username else {"email":username}
        try:
            user = User.objects.get(**user_data)
        except User.DoesNotExist:
            raise serializers.ValidationError({"username":"Account with username does not exist"})  
        if user.is_active:
            raise serializers.ValidationError({"account":"Account is already active"})  
        data['user'] = user
        return data



    def save(self):
        request = self.context.get('request')
        user = self.validated_data.get('user')
        test_data = Email(request,user).send_common_activation_mail()
        # returns the needed test_data if we are using 
        # the testserver else it just sends the email
        if test_data: 
            self.validated_data["uidb64"] = test_data.get('uidb64')
            self.validated_data["token"]=test_data.get('token')









class ResetPasswordMailSerializer(serializers.Serializer):
    username = serializers.CharField(write_only=True)
    # note that email field is read only i.e it's only sent out 
    email = serializers.CharField(read_only=True)
    uidb64 = serializers.CharField(read_only=True)
    token = serializers.CharField(read_only=True)

    class Meta:
        fields = ("username","email","uidb64","token")


    def validate(self,data):
        username = data.get("username").lower()
        user_data = {"username":username} if "@" not in username else {"email":username}
        try:
            user = User.objects.get(**user_data)
        except User.DoesNotExist:
            raise serializers.ValidationError({"username":"No user with that username or email exists"})
        data['user'] = user
        return data

    def save(self):
        request = self.context.get('request')
        user = self.validated_data.get("user")
        test_data = Email(request,user).send_common_reset_password_mail()
        self.validated_data['email'] = get_asterisked_mail(user.email)
        if test_data:
            self.validated_data["uidb64"] = test_data.get("uidb64")
            self.validated_data["token"] = test_data.get("token")
        