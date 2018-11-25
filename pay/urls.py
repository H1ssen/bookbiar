from django.urls import path

from . import views

app_name = 'pay'

urlpatterns = [
    path('Buy/',views.Buy,name='buy'),
    path('Verify/',views.Verify,name='verify'),

]