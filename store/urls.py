from django.urls import path
from store import views

urlpatterns = [

    path('home/',views.Home.as_view(),name="home"),
    path('list_product/<int:pk>',views.ProductView.as_view(),name="product_list"),
    path('products_data/<int:pk>',views.ProductDetail.as_view(),name="product_data"),
    path('register/',views.RegisterView.as_view(),name="register"),
    path('signin/',views.SigninView.as_view(),name="signin"),
    path('signout/',views.SignOut.as_view(),name="signout"),
    path('cart/<int:pk>',views.AddtoCartView.as_view(),name="cart"),
    path('cart/delete/<int:pk>',views.CartDelete.as_view(),name="cart_delete"),
    path('cart_details/',views.CartDetails.as_view(),name="cart_detail"),
    path('order/<int:pk>',views.OrderView.as_view(),name="order"),
    path('orderlist/',views.OrderList.as_view(),name="orderlists"),
    path('order/delete/<int:pk>',views.RemoveOrder.as_view(),name="oder_delete")

]