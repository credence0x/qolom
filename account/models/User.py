from django.contrib.auth.models import AbstractUser

class User(AbstractUser):

    def has_related_user_profile_object(self):
        try:
            bool(self.userProfile)
        except AttributeError:
            return False
        return True


    def has_related_business_profile_object(self):
        try:
            bool(self.businessProfile)
        except AttributeError:
            return False
        return True