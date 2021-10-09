from django.urls import path
from django.conf.urls import include, re_path
from . import views

app_name = "dashboard"


urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('qr-view/', views.CreateQRView.as_view(), name='qr_generate'),
    path('qr-list/', views.ListQRView.as_view(), name='qr_list'),
    path('create-category/', views.CreateCategory.as_view(), name='create_category'),
    path('category-list/', views.CategoryList.as_view(), name='category_list'),
    path('category-update/<pk>/', views.UpdateCategory.as_view(), name='category_update'),
    path('delete/<pk>/', views.DeleteCategory, name="category_delete"),
    path('create-menu/', views.CreateMenu.as_view(), name='create_menu'),
    path('menu-list/', views.MenuList.as_view(), name='menu_list'),
    path('menu-update/<pk>/', views.UpdateMenu.as_view(), name='menu_update'),
    path('menu-delete/<pk>/', views.DeleteMenu, name="menu_delete"),
    path("genarate-qr/", views.generateQr, name="generateQr")
]
