from rest_framework import serializers
from io import BytesIO
from PIL import Image
from django.core.files import File

def ensure_user_has_related_business_profile_object(user):
    """
    Confirms that a user has a related BusinessProfile object
    """
    if not user.has_related_business_profile_object():
        raise serializers.ValidationError({"account":"This is not a business account. \
                                                    Please try using theend user sign up page "})


def compress_image(image):
    im = Image.open(image)
    if im.mode != 'RGB':
        im = im.convert('RGB')
    im_io = BytesIO()
    # resize image to 300 by 300
    im = im.resize((300,300),Image.ANTIALIAS ) 
    im.save(im_io, 'JPEG', quality=70) 
    new_image = File(im_io, name=image.name)
    return new_image