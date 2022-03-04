from account.models.UserProfile import UserProfile
from account.module.generate_random import getRandomKey
from business.models import BusinessQueue
from rest_framework import serializers



class QueueUserProfileSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
                                        read_only=True,
                                        slug_field='first_name'
                                    )
    class Meta:
        model = UserProfile
        fields = ("user","ticket")
        depth = 2


class CreateQueueSerializer(serializers.ModelSerializer):

    class Meta:
        model = BusinessQueue
        fields = ("name","instruction","information","id")

    

    def create(self,validated_data):
        validated_data['owner'] = self.context.get("request").user.businessProfile 
        validated_data['key'] = getRandomKey(8) 
        queue = BusinessQueue.objects.create(**validated_data)
        return queue 
    



class RetrieveQueueSerializer(serializers.ModelSerializer):
    people_on_queue =  serializers.SerializerMethodField()
    class Meta:
        model = BusinessQueue
        fields = ("people_on_queue",)

    def get_people_on_queue(self, instance):
        """
        Method to get the people on the
        queue based on time of entry
        """
        people = instance.people_on_queue.all().order_by('-time_of_queue_entry')
        return QueueUserProfileSerializer(people, many=True).data





class RetrieveQueueInformationSerializer(serializers.ModelSerializer):
    """
    Serializer to get information about the Businessqueue
    """
    # number of people on the Businessqueue
    num_of_people = serializers.SerializerMethodField()
    class Meta:
        model = BusinessQueue
        fields =  ("name","instruction","information","num_of_people")

    def get_num_of_people(self,obj):
        return obj.people_on_queue.all().count()


class UpdateDestroyQueueSerializer(serializers.ModelSerializer):    

    class Meta:
        model = BusinessQueue
        fields = ("name","instruction","information",)