from django.urls import path

from business.api import (
                                    CreateCalendarAPIView,
                                    RetrieveUpdateDestroyCalendarAPIView,

                                    CreateQueueAPIView,
                                    RetrieveQueueAPIView,
                                    UpdateDestroyQueueAPIView,
                                    RetrieveQueueInformationAPIView
                                )


# from business.views import ResendConfirmationView,activateBankView,DelPaymentView,DaysOpenView,CreateLineView,OrderDetailView,OrdersView,PaymentView,EditItemView,ItemsView,business_ajax, BusinessHomePageView, LineDetailView,EditLineView,ChangePasswordView,DeleteBusinessLineView


app_name ='business'
urlpatterns = [

        path('calendar/add/', CreateCalendarAPIView, name='calendar_add' ),
        path('calendar/update/', RetrieveUpdateDestroyCalendarAPIView, name='calendar_update' ),
        path('calendar/delete/', RetrieveUpdateDestroyCalendarAPIView, name='calendar_delete' ),
        path('calendar/', RetrieveUpdateDestroyCalendarAPIView, name='calendar_view' ),


        path('queue/<int:pk>/info/', RetrieveQueueInformationAPIView, name='queue_view_info' ),
        path('queue/<int:pk>/update/', UpdateDestroyQueueAPIView, name='queue_update' ),
        path('queue/<int:pk>/delete/', UpdateDestroyQueueAPIView, name='queue_delete' ),
        path('queue/<int:pk>/', RetrieveQueueAPIView, name='queue_view' ),
        path('queue/add/', CreateQueueAPIView, name='queue_add' ),

#     re_path(r'^add-line/$', CreateLineView, name='business_line' ),
#     re_path(r'^$', BusinessHomePageView, name='business_homepage' ),
#     # add business name in url and views
#     re_path(r'^line/(?P<slug>[-\w\s\d]+)/$',
#             LineDetailView,
#             name='business_detailview' ),
#     # next urlshould allow for numbers too
#     re_path(r'^edit-line/(?P<slug>[-\w\s\d]+)/$', EditLineView, name ='edit_line'),
#     re_path(r'^change-password/$', ChangePasswordView, name ='change_password'),
#     re_path(r'^delete-line/$', DeleteBusinessLineView , name ='delete_line'),
#     re_path(r'^(?P<uniquefield>[\w]{7,8})/$', business_ajax , name ='business_ajax'),
#     re_path(r'^bank-confirmation/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,100})/$',
#             activateBankView, name='bank_confirmation' ),
#     re_path(r'^edit-item/(?P<identity>[\w]+)/$', EditItemView, name='edit_item' ),
#     re_path(r'^items/$', ItemsView, name='items' ),
#     re_path(r'^orders/$', OrdersView, name='orders' ),
#     re_path(r'^resend-bank-confirmation-email/$',
#             ResendConfirmationView, name='resend_bank_confirm' ),
    
#     re_path(r'^business-hours/$', DaysOpenView, name='business_hours' ),
#     re_path(r'^order-detail/(?P<identity>[\w]+)/$',
#             OrderDetailView, name='order_detail' ),
   
#     re_path(r'^payment-information/$', PaymentView, name='payment' ),
#     re_path(r'^delete-payment-information/$', DelPaymentView, name='del_pay' ),
]
