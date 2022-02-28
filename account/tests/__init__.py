
from .businessProfile.businessProfile import   (
                                            CreateBusinessProfileTests,
                                            UpdateBusinessProfileTests,
                                        )
from .businessProfile.authentication import (
                                            AuthenticateBusinessProfileTests,
                                            DeauthenticateBusinessProfileTests,
                                            ActivateBusinessProfileTokenTests,

                                        )

from .userProfile.userProfile import   (
                                            CreateUserProfileTests,
                                            UpdateUserProfileTests,
                                        )
from .userProfile.authentication import (
                                            AuthenticateUserProfileTests,
                                            DeauthenticateUserProfileTests,
                                            ActivateUserProfileTokenTests,

                                        )
from .mail import (SignUpConfirmationEmailTests)
from .update import ResetPasswordTests