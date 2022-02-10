from account.api.userProfile.userProfile import (
                                                  CreateUserProfileAPIView,
                                                  UpdateUserProfileAPIView,
                                                )

from account.api.userProfile.authentication import (
                                                     AuthenticateUserProfileAPIView,
                                                     DeauthenticateUserProfileAPIView,
                                                   )

from account.api.userProfile.email import (
                                            SignUpConfirmationEmailAPIView
                                            )                               