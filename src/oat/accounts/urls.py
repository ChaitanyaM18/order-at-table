from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf.urls import include, re_path
from . import views
from .forms import CustomAuthenticationForm
from django.views.decorators.csrf import csrf_exempt

app_name = "accounts"

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('resetpassword/', views.ResetPassword.as_view(), name='resetpassword'),
    path('passwordchange/', views.send_email, name="send_email"),
    path('passwordview/', views.PasswordView.as_view(), name='password_view'),
    path('password/', views.change_password, name='change_password'),
    path('password-done/', views.PasswordDone.as_view(), name='password_done'),
    path('emailexists/', views.emailexists, name='emailexists'),
    path('create-user/', views.UserCreateView.as_view(), name='create_user'),
    path('changepassword/', views.PasswordChange.as_view(), name='changepassword'),
    path('users_list/', views.UserListView.as_view(), name='users_list'),
    path('view/<int:pk>/', views.UserDetail.as_view(), name="view_user"),
    path('update/<int:pk>/', views.UserUpdateView.as_view(), name="update_user"),
    path('delete_user/', views.UserDeleteView.as_view(), name="delete_user"),
    path('profilesettings/', views.django_image_and_file_upload_ajax, name='profilesettings'),
    path('createpassword/', views.createrandompassword, name='createpassword'),
    path('check_old_password/', views.check_current_password, name='check_old_password'),
    path('profile/', views.ProfileView, name="profile"),

]
