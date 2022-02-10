from .userProfile.userProfile import (
                                 UserProfileSerializer,
                                 CreateUserProfileSerializer,
                                 UpdateUserProfileSerializer,
                            )
from .userProfile.authentication import (
                                AuthenticateUserSerializer,
                                DeauthenticateUserSerializer,
                            )
from .userProfile.email import (
                                SignUpConfirmationEmailSerializer,
                            )