from queue import Queue
from account.models.UserProfile import UserProfile
from account.module.generate_random import getRandomKey
from business.models.Queue import Queue
from rest_framework import serializers



class __QueueUserProfileSerializer(serializers.ModelSerializer):
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
        model = Queue
        fields = ("name","instruction","information",)

    

    def create(self,validated_data):
        validated_data['owner'] = self.context.get("request").user.businessProfile 
        validated_data['key'] = getRandomKey(8) 
        queue = Queue.objects.create(**validated_data)
        return queue 
    



class RetrieveQueueSerializer(serializers.ModelSerializer):
    people_on_queue =  serializers.SerializerMethodSerializer()
    class Meta:
        model = Queue
        fields = ("people_on_queue",)

    def get_people_on_queue(self, instance):
        """
        Method to get the people on the
        queue based on time of entry
        """
        people = instance.people_on_queue.all().order_by('-time_of_queue_entry')
        return __QueueUserProfileSerializer(people, many=True).data





class RetrieveQueueInformationSerializer(serializers.ModelSerializer):
    """
    Serializer to get information about the queue
    """
    # number of people on the queue
    num_of_people = serializers.SerializerMethodField()
    class Meta:
        model = Queue
        fields =  ("name","instruction","information","num_of_people")

    def get_num_of_people(self,obj):
        return obj.people_on_queue.all().count()


class UpdateDestroyQueueSerializer(serializers.ModelSerializer):    

    class Meta:
        model = Queue
        fields = ("name","instruction","information",)


      
    