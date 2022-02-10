
from logging.config import valid_ident
from account.serializers import UserProfileSerializer
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import login,logout
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from account.tokens import account_activation_token
from django.core.mail import send_mail
from django.template import loader


class SignUpConfirmationEmailSerializer(serializers.Serializer):
    username = serializers.CharField(write_only=True)

    class Meta:
        fields = ("username")

    

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
        request = self.context.get("request")
        validated_data = self.validated_data
        user = validated_data.get("user")
        current_site = get_current_site(request)
        mail_subject = 'Activate Your Account.'
        plain_message = render_to_string('account/authentication/confirm_registration.html', {
                                            'user': user,
                                            'domain': current_site.domain,
                                            'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                                            'token':account_activation_token.make_token(user),
                                            })
        to_email = user.email
        html_message = loader.render_to_string('account/authentication/confirm_registration.html',
                                                {'user': user,
                                                'domain': current_site.domain,
                                                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                                                'token':account_activation_token.make_token(user),
                                                })
        # print(f"http://localhost:8000/{urlsafe_base64_encode(force_bytes(user.pk))}/{account_activation_token.make_token(user)}")     
        
        send_mail(
                    mail_subject,
                    plain_message,
                    'Qolom <auth@qolom.com>',
                    [to_email,],
                    html_message = html_message,
                    fail_silently=False
                 )
        
