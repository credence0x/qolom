from django.urls import path

from business.api import (
                                    RetrieveUpdateCalendarAPIView,

                                    CreateQueueAPIView,
                                    RetrieveQueueAPIView,
                                    UpdateQueueAPIView,
                                    DestroyQueueAPIView,
                                    RetrieveQueueInformationAPIView,


                                    CreateBankAPIView,
                                    ResolveBankAPIView,
                                    ConfirmBankAPIView,
                                    ListBankAPIView,

                                     CreateItemAPIView,
                                     ListItemAPIView,
                                     UpdateItemAPIView,
                                     RetrieveItemAPIView,
                                     DestroyItemAPIView,

                                     OrderListAPIView,
                                     OrderUpdateStatusAPIView,
                        )




app_name ='business'
urlpatterns = [

        path('calendar/update/', RetrieveUpdateCalendarAPIView.as_view(), name='calendar_update' ),
        path('calendar/', RetrieveUpdateCalendarAPIView.as_view(), name='calendar_view' ),

        path('queue/info/<int:pk>/update/', UpdateQueueAPIView.as_view(), name='queue_info_update' ),
        path('queue/info/<int:pk>/', RetrieveQueueInformationAPIView.as_view(), name='queue_info_view' ),
        
        path('queue/<int:pk>/delete/', DestroyQueueAPIView.as_view(), name='queue_delete' ),
        path('queue/<int:pk>/', RetrieveQueueAPIView.as_view(), name='queue_view' ),
        path('queue/add/', CreateQueueAPIView.as_view(), name='queue_add' ),



        path('bank/add/', CreateBankAPIView.as_view(), name='bank_add' ),
        path('bank/resolve/', ResolveBankAPIView.as_view(), name='bank_resolve' ),
        path('bank/confirm/', ConfirmBankAPIView.as_view(), name='bank_confirm' ),
        path('bank/', ListBankAPIView.as_view(), name='bank_list' ),


        path('item/<int:pk>/update/', UpdateItemAPIView.as_view(), name='item_update' ),
        path('item/<int:pk>/delete/', DestroyItemAPIView.as_view(), name='item_delete' ),
        path('item/<int:pk>/', RetrieveItemAPIView.as_view(), name='item_retrieve' ),
        path('item/create/', CreateItemAPIView.as_view(), name='item_add' ),
        path('item/', ListItemAPIView.as_view(), name='item_list' ),



        path('order/update-status/<int:pk>/', OrderUpdateStatusAPIView.as_view(), name='order_update_status' ),
        path('order/', OrderListAPIView.as_view(), name='order_list' ),

]