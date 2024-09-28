from django.urls import path
from . import views
urlpatterns = [
    path('',views.cart,name='cart'),
    path('add_cart/<int:product_id>/',views.add_cart,name = 'add_cart'),
    # path('add_cart_at/<int:product_id>/',views.add_cart_at,name = 'add_cart_at'),
    path('view_cart/',views.view_cart,name = 'view_cart'),
    path('remove_item/<int:product_id>/<int:cart_item_id>/',views.remove_item,name = 'remove_item'),
    path('delete_item/<int:product_id>/<int:cart_item_id>/',views.delete_item,name='delete_item'),
    path('checkout/',views.checkout,name='checkout'),
    
]
