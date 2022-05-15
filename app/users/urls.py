from django.urls import path
from users.api import (
                        OrderAPIView,
                        OrderCreateAPIView,
                        OrderVerifyPaymentAPIView,
                        OrderInitializePaymentAPIView,
                        OrderPaymentWithSavedCardAPIView,
                        OrderPaystackWebhookAPIView,

                        CreateCardAPIView,
                        RetrieveUpdateDestroyCardAPIView,

        )



app_name='users'
urlpatterns = [
    path('card/', CreateCardAPIView.as_view(), name='card_create_or_list'),
    path('card/<int:pk>/', RetrieveUpdateDestroyCardAPIView.as_view(), name='card_retrieve_update_or_delete'),

    path('order/create/', OrderCreateAPIView.as_view(), name='order_add'),
    path('order/initialize/', OrderInitializePaymentAPIView.as_view(), name='order_initialize'),
    path('order/verify/', OrderVerifyPaymentAPIView.as_view(), name='order_verify'),
    path('order/pay-with-card/', OrderPaymentWithSavedCardAPIView.as_view(), name='order_pay_with_card'),
    path('order/', OrderAPIView.as_view(), name='order_list'),


    path('paystack/webhook/', OrderPaystackWebhookAPIView.as_view(), name='paystack_webhook'),

]
