from django.urls import path
from django.conf.urls import include, re_path
from . import views

app_name = "orders"

urlpatterns = [
path('', views.CreateUserDetail.as_view(), name='create_user'),
path('categories/', views.CategoryView.as_view(), name='categories'),
path('menu_list/<pk>/', views.MenuList.as_view(), name='menu_list'),
path('cart/', views.CartView.as_view(), name='cart'),
path('checkout/', views.checkout, name='checkout'),
path("view-orders/", views.view_orders, name="view_orders"),
path("exit/", views.view_orders, name="exit"),

]
