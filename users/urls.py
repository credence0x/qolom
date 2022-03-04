# from django.urls import path,re_path
# from .views import UserHomePageView,GetLocationView,ManageCardView,RemoveCardView,PayWithCardView,SaveCardView,CheckReadyAPIView,OrdersListView,OrderView,CheckOutView,UserMenuView,CheckKeyView,special_ajax,user_ajax,user_line,SpecialLineDetailView,CreateSpecialLineView,EditSpecialLineView, UserDetailView,SearchPageView,EditView,ChangePasswordView,FavouritesView
# from django.views.decorators.cache import cache_page



app_name='users'
urlpatterns = [
#     re_path(r'^$', UserHomePageView, name='user_homepage'),
#     re_path(r'^add-special-line/$', CreateSpecialLineView, name='create_line' ),
#     re_path(r'^key/$',  CheckKeyView, name='key'),
#     re_path(r'^b/(?P<key>[\w]{7})/(?P<slug>[-\w]+)$',
#             UserDetailView, name='user_detailview'),
#     re_path(r'^loc_info/$',GetLocationView, name='get_location'),
#     re_path(r'^items/(?P<key>[\w]{7})/$',
#             UserMenuView, name='show_items'),
#     re_path(r'^checkout/(?P<key>[\w]{7})/$',
#             CheckOutView, name='checkout'),
#     re_path(r'^view-order/(?P<identity>[\w]{1,1000})/$',
#             OrderView, name='order'),
#     re_path(r'^orders-list/$',
#             OrdersListView, name='orders_list'),
#     re_path(r'^line/(?P<unumber>[\w]{7,8})/$',
#             user_line,
#             name='line' ),
#     re_path(r'^pay-with-card/(?P<the_id>[\w]{2,1000})/(?P<signature>[\w]{2,1000})/$',
#             PayWithCardView,
#             name='pay-with-card' ),
    
#     re_path(r'^check_ready/$', CheckReadyAPIView, name='check_ready' ),
#     #remember to add hashtags sand stuff
#     re_path(r'^save-card/$', SaveCardView, name='save_card' ),
#     re_path(r'^remove-card/$', RemoveCardView, name='remove_card'),
#     re_path(r'^manage-cards/$', ManageCardView, name='manage_cards'),
    
    
#     re_path(r'^f/$',SearchPageView, name ='search'),
#     re_path(r'^edit-special-line/$',EditSpecialLineView, name ='edit_line'),
#     re_path(r'^favourites/$',FavouritesView, name ='favourites'),
#     re_path(r'^x/(?P<uniquefield>[\w]{7,8})/(?P<unique>[\w]{7})/$',
#             user_ajax, name = 'user_ajax'),
#     re_path(r'^s/$',special_ajax, name = 'special_ajax'),
 
    
#     re_path(r'^edit-profile/$', EditView, name ='user_edit'),
#     re_path(r'^change-password/$', ChangePasswordView, name ='change_password'),
#     re_path(r'^special-line/$',
#             SpecialLineDetailView,
#             name='special_detailview' ),
#     # next urlshould allow for numbers too
    
    
]
# #dont forget encode and decode countries.js staates e.g korc5e
