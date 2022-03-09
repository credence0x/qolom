from account.models.BusinessProfile import BusinessProfile
from business.models.Bank import Bank
from rest_framework import serializers
from core.module.email import Email
from core.module.paystack import Paystack
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_text
from account.tokens import account_activation_token_two

User = get_user_model()


"""
    Bank Serializers
"""


class BankSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    # uidb64 and token are for tests
    uidb64 = serializers.CharField(read_only=True,required=False)
    token = serializers.CharField(read_only=True,required=False)

    class Meta:
        model = Bank
        fields = (
                    "owner",
                    "account_number",
                    "bank_name",
                    "bank_code",
                    "account_name",
                    "password",

                    "uidb64",
                    "token"
                )

    def validate(self,data):
        password = data.get("password")
        owner = data.get("owner")
        user = owner.user
        if not user.check_password(password):
            raise serializers.ValidationError({"password":"Incorrect Password"})
        
        del data["password"]
        return data
    
    def create(self,validated_data):
        request  = self.context.get("request")
        user = request.user  
        bank = Bank.objects.create(**validated_data)
        test_data = Email(request,user).send_business_bank_confirmation_mail()
        if test_data: 
            self.validated_data["uidb64"] = test_data.get('uidb64')
            self.validated_data["token"]=test_data.get('token')
        return self.validated_data


class ResolveBankSerializer(serializers.Serializer):
    """
    Confirm that an account belongs to the right customer
    """
    account_number = serializers.CharField(write_only=True)
    bank_code = serializers.CharField(write_only=True)

    data = serializers.DictField(read_only=True,child=serializers.CharField())

    class Meta:

        fields = (
            "account_number",
            "account_name",
            "bank_code",
            "data"
        )

    def save(self):
        validated_data = self.validated_data
        account_number = validated_data.get("account_number")
        bank_code = validated_data.get("bank_code")
        data = Paystack().resolve_bank(account_number,bank_code)
        if not data:
            raise serializers.ValidationError("Incorrect Details")
        self.validated_data["data"] = data
        return 



class ConfirmBankSerializer(serializers.Serializer):
    uidb64 = serializers.CharField()
    token = serializers.CharField()
    class Meta:

        fields = (
            "uidb64",
            "token",
        )

    def validate(self,data):
        uidb64 = data.get("uidb64")
        token = data.get("token")

        try:
            user_id = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)
            data['user'] = user
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise serializers.ValidationError("Invalid Token")
        
        if not account_activation_token_two.check_token(user, token):
            raise serializers.ValidationError("Invalid Token")
        return data
        
    def save(self):
        user = self.validated_data.get("user")
        bank = user.businessProfile.bank 
        if Paystack().add_transfer_recipient(user):
            bank.activated = True
            # implement send notification email to business
            bank.save()
        else:
            raise serializers.ValidationError("Please try again")



