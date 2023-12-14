from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

app_name = "account"


urlpatterns = [
    # Authenticating urls
    path('user/login/', views.UserLogin.as_view(), name="user_login"),
    path('user/logout/', views.UserLogout.as_view(), name="user_logout"),
    path('user/register/', views.UserRegisterView.as_view(), name="user_register"),
    path('otp/<str:token>/', views.UserCheckOtp.as_view(), name="check_otp"),
    path('user/delete-account/', views.UserDeleteAccount.as_view(), name="user_delete_account"),

    # Token 
    path('token/', views.TokenObtainView.as_view(), name='token_obtain'),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),

    # Profile, Panel, user managments
    path('user/profile/<str:username>/<slug:slug>/', views.UserProfileView.as_view(), name="user_profile"),
    path('user/change-password/', views.UserChangePasswordView.as_view(), name="user_change_password")
]