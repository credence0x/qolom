"""standin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,re_path, include
from account.views import LoginView,LogoutView,LandingPageView,termsView,privacyView
from users.views import VerifyPaymentScriptView,webhook

urlpatterns = [
    re_path(r'^accounts/', include('account.urls', namespace='account')),
    re_path(r'^b/', include('business.urls', namespace='business')),
    re_path(r'^u/', include('users.urls', namespace='users')),
    re_path(r'^$', LandingPageView, name='landing-page' ),
    re_path(r'^login$', LoginView, name='login' ),
    
    re_path(r'^verify-script/$', VerifyPaymentScriptView, name='verify' ),
    re_path(r'^legal-terms-of-use/$', termsView, name='terms-of-use' ),
    re_path(r'^privacy-policy/$', privacyView, name='privacy-policy' ),
    path('paystack', include(('paystack.frameworks.django.urls','paystack'),namespace='paystack')),
    re_path(r'^log-out$', LogoutView, name='logout' ),
    re_path(r'^webhook$', webhook, name='webhook' ),
    #there are two login urls

]
