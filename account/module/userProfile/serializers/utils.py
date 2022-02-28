from rest_framework import serializers
def ensure_user_has_related_user_profile_object(user):
    """
    Confirms that a user has a related UserProfile object
    """
    if not user.has_related_user_profile_object:
        raise serializers.ValidationError({"account":"This is not an end user account. \
                                                    Please try using the business sign up page "})
