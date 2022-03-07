from account.models.UserProfile import CardInformation
from rest_framework import serializers

class CardSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CardInformation
        fields = "__all__"


    