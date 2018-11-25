from django.urls import path
from . import views
from django.urls import include
app_name = 'user'

urlpatterns = [
    path('Register/',views.registerUser.as_view(),name='register'),
    path('Validate/',views.ValidateCode.as_view(),name='validate'),
    path('fillInfo/',views.FillInfo.as_view(),name='fillInfo'),
    path('checkUsername/',views.checkUsername,name='checkusername'),
    path('check/',views.checkData,name='check'),
    path('getCaptcha/',views.getCaptcha,name='captcha'),
    path('Login/',views.Login.as_view(),name='login'),
    path('Logout/',views.Logout,name='logout'),
    path('setProfilePic/',views.setProfilePic,name='setProfilePic')
]