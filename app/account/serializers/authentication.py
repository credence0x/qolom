from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.utils.encoding import force_text
from account.tokens import account_activation_token_three
from django.utils.http import urlsafe_base64_decode

User = get_user_model()

class CheckResetPasswordLinkSerializer(serializers.Serializer):
    uidb64 = serializers.CharField(write_only=True)
    token = serializers.CharField(write_only=True)
    
    class Meta:
        fields = ("uidb64","token")

    def validate(self,data):
        uidb64 = data.get("uidb64")
        token = data.get("token")

        try:
            user_id = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise serializers.ValidationError("Invalid Token")
        
        if not account_activation_token_three.check_token(user, token):
            raise serializers.ValidationError("Invalid Token")
        return data
        
    def save(self):
        pass
