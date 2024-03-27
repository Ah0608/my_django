from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView

from app_01.views import RegisterView, CheckUsernameView, Logoutview, IndexView, sendmeail, LoginView

urlpatterns = [
    path('index/', IndexView.as_view(),name='index'),
    path('register/', RegisterView.as_view(),name='register'),
    path("login/", LoginView.as_view(),name='login'),
    path("logout/", Logoutview.as_view(),name='logout'),
    path("sendmeail/", sendmeail.as_view(),name='sendmeail'),
    path('captcha/', include('captcha.urls'),name='captcha'),   # 增加这一行
    path('checkusername/', CheckUsernameView.as_view(), name='checkusername'),
]
