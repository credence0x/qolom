from business.models.Calendar import Calendar
from rest_framework import serializers
from business.module import variables 
        

class RetrieveUpdateCalendarSerializer(serializers.ModelSerializer):    

    class Meta:
        model = Calendar
        exclude = ("owner","is_active","activated_at","deactivated_at")

      
    def validate(self,data):
        for day in variables.LIST_OF_DAYS:
            open_time = data.get(f"{day}_o", None)
            closing_time = data.get(f"{day}_c", None)
        
            if open_time and closing_time:
                # ensure that the open time and 
                # closing time do not overlap
                if  closing_time <= open_time:
                    raise serializers.ValidationError(f"Business closes before it opens on {variables.FULL_WEEKDAYS[day].upper()}")
            else:
                # ensure that if the opening time is filled, 
                # the closing time must be filled also
                # or ensure that both are null
                if (not closing_time and open_time ) or (not open_time and closing_time):
                    # if either closing or opening time is null but not both
                    raise serializers.ValidationError(f"Both fields should be null or filled out for {variables.FULL_WEEKDAYS[day].upper()}")

        return data