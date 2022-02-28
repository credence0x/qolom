from account.api.userProfile.userProfile import (
                                                  CreateUserProfileAPIView,
                                                  UpdateUserProfileAPIView,
                                                )

from account.api.userProfile.authentication import (
                                                    ActivateUserProfileTokenAPIView,
                                                     AuthenticateUserProfileAPIView,
                                                     DeauthenticateUserProfileAPIView,
                                                   )

from account.api.businessProfile.businessProfile import (
                                                  CreateBusinessProfileAPIView,
                                                  UpdateBusinessProfileAPIView,
                                                )

from account.api.businessProfile.authentication import (
                                                    ActivateBusinessProfileTokenAPIView,
                                                     AuthenticateBusinessProfileAPIView,
                                                     DeauthenticateBusinessProfileAPIView,
                                                   )

from account.api.mail import (SignUpMailAPIView,
                              ResetPasswordMailAPIView)

from account.api.update import (ResetPasswordAPIView)                            
from account.api.authentication import (CheckResetPasswordLinkAPIView)                          