from django.urls import path,re_path

from account.api  import (
                          CreateUserProfileAPIView,
                          UpdateUserProfileAPIView,
                        )

from account.api import (
                           AuthenticateUserProfileAPIView,
                           DeauthenticateUserProfileAPIView,
                        )

from .views import activateView,changeEmail,set_new_passwordView,ResetPasswordView,activate_resetView,UserAccountView,confirm_emailView,BusinessAccountView,EditBusinessProfileView



app_name='account'
urlpatterns = [
####################################################################
        # APIs
    path('user-profile/create/', CreateUserProfileAPIView.as_view(), name='create_user_profile' ),
    path('user-profile/<int:pk>/update/', UpdateUserProfileAPIView.as_view(), name='update_user_profile' ),
    path('user-profile/authenticate/', AuthenticateUserProfileAPIView.as_view(), name='authenticate_user_profile' ),
    path('user-profile/deauthenticate/', DeauthenticateUserProfileAPIView.as_view(), name='deauthenticate_user_profile' ),

#####################################################################
    re_path(r'^user-signup/$', UserAccountView, name='user_signup' ),
    re_path(r'^change-email/$', changeEmail, name='change_email' ),
    re_path(r'^confirm-email/$', confirm_emailView, name='confirm_html' ),
    re_path(r'^forgot-password/$', ResetPasswordView, name='forgot_password' ),
    re_path(r'^password-reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,100})/$',
            activate_resetView, name='activate_reset' ),
    re_path(r'^set-password/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,100})/$', set_new_passwordView, name='set_new_password' ),
    re_path(r'^business-signup/$', BusinessAccountView, name='business_signup' ),
    re_path(r'^edit-business-profile/$', EditBusinessProfileView, name='edit_business_registration' ),
    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,100})/$',
        activateView, name='activate'),
  
]
