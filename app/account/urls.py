from django.urls import path,re_path

from account.api  import (
                          CreateUserProfileAPIView,
                          UpdateUserProfileAPIView,
                          ActivateUserProfileTokenAPIView,
                          AuthenticateUserProfileAPIView,
                          DeauthenticateUserProfileAPIView,


                          CreateBusinessProfileAPIView,
                          ListBusinessProfileAPIView,
                          UpdateBusinessProfileAPIView,
                          ActivateBusinessProfileTokenAPIView,
                          AuthenticateBusinessProfileAPIView,
                          DeauthenticateBusinessProfileAPIView,


                          SignUpMailAPIView,
                          ResetPasswordMailAPIView,
                          ResetPasswordAPIView,
                          CheckResetPasswordLinkAPIView,   

                          ChangePasswordAPIView,   
                        )





app_name='account'
urlpatterns = [
                             # APIs

    # user-profile
    path('user-profile/create/', CreateUserProfileAPIView.as_view(), name='create_user_profile' ),
    path('user-profile/<int:pk>/update/', UpdateUserProfileAPIView.as_view(), name='update_user_profile' ),
    path('user-profile/activate/', ActivateUserProfileTokenAPIView.as_view(), name='activate_user_profile' ),
    path('user-profile/authenticate/', AuthenticateUserProfileAPIView.as_view(), name='authenticate_user_profile' ),
    path('user-profile/deauthenticate/', DeauthenticateUserProfileAPIView.as_view(), name='deauthenticate_user_profile' ),
    

     # business-profile
    
    path('business-profile/create/', CreateBusinessProfileAPIView.as_view(), name='create_business_profile' ),
    path('business-profile/<int:pk>/update/', UpdateBusinessProfileAPIView.as_view(), name='update_business_profile' ),
    path('business-profile/activate/', ActivateBusinessProfileTokenAPIView.as_view(), name='activate_business_profile' ),
    path('business-profile/authenticate/', AuthenticateBusinessProfileAPIView.as_view(), name='authenticate_business_profile' ),
    path('business-profile/deauthenticate/', DeauthenticateBusinessProfileAPIView.as_view(), name='deauthenticate_business_profile' ),
    
    # search for business
    path('business-profile/', ListBusinessProfileAPIView.as_view(), name='list_business_profile' ),


    # common 
    path('mail/confirm-sign-up/', SignUpMailAPIView.as_view(), name='mail_confirm_sign_up' ),  
    path('mail/reset-password/', ResetPasswordMailAPIView.as_view(), name='mail_reset_password' ),
    
    path('reset-password/validate-link/', CheckResetPasswordLinkAPIView.as_view(), name='reset_password_link_check' ),
    path('reset-password/', ResetPasswordAPIView.as_view(), name='reset_password' ),
    
    path('change-password/', ChangePasswordAPIView.as_view(), name='change_password' ),

]
