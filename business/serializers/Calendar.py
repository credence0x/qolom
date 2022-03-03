from business.models.Calendar import Calendar
from rest_framework import serializers
from business.module import variables 
        

def common_validation_function(data):
    for day in variables.LIST_OF_DAYS:
        open_time = data.get(f"{day}_o", None)
        closing_time = data.get(f"{day}_c", None)

        # ensure that if the opening time is filled, 
        # the closing time must be filled also
        if  (not open_time) or (not closing_time):
            raise serializers.ValidationError(f"Fill out all information for {variables.FULL_WEEKDAYS[day]}")

        # ensure that the open time and 
        # closing time do not overlap
        if  closing_time <= open_time:
            raise serializers.ValidationError(f"Business closes before it opens on {variables.FULL_WEEKDAYS[day]}")



class CreateCalendarSerializer(serializers.ModelSerializer):

    class Meta:
        model = Calendar
        exclude = ("owner",)

    def validate(self,data):
        common_validation_function(data)
        return data

    def create(self,validated_data):
        validated_data['owner'] = self.context.get("request").user.businessProfile 
        calendar = Calendar.objects.create(**validated_data)
        return calendar 
    



class RetrieveUpdateDestroyCalendarSerializer(serializers.ModelSerializer):    

    class Meta:
        model = Calendar
        exclude = ("owner",)

      
    def validate(self,data):
        common_validation_function(data)
        return data