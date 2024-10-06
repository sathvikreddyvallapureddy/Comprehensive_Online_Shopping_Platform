from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('watches',views.watches, name='watches'),
    path('about',views.about, name='about'),
    path('contact',views.contact, name='contact'),
    path('watches/<str:title>',views.watch_detail, name='watch_detail'),
    path('cart',views.cart, name="cart"),
    path('wishlist',views.wishlist, name="wishlist"),
    path('myaccount',views.myaccount, name="myaccount"),
    path('signup',views.signup, name="signup"),
    path('signin',views.signin, name="signin"),
    path('signout',views.signout, name="signout"),

    path('product-list', views.productlistAjax),
    path('search', views.search, name="search"),
    
    path('add-to-cart', views.addtocart, name="addtocart"),
    path('update-cart', views.updatecart, name="updatecart"),
    path('delete-cart-item', views.deletecartitem, name="deletecartitem"),
    path('delete-wishlist-item', views.deletewishlistitem, name="deletewishlistitem"),
    path('move-to-wishlist', views.movetowishlist, name="movetowishlist"),
    path('checkout', views.checkout, name="checkout"),
    path('placeorder', views.placeorder, name="placeorder"),
    path('proceed-to-pay', views.proceedtopay, name="proceedtopay"),

    path('my-orders', views.myorders, name="myorders"),
    path('vieworder/<str:tracking_no>', views.vieworder, name="vieworder"),
    path('forgotpassword', views.forgotpassword, name="forgotpassword"),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)