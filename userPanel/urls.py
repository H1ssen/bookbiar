from django.urls import path
from . import views
app_name = 'userPanel'

urlpatterns = [
    path('Info/',views.info.as_view(),name='info'),
    path('',views.info.as_view(),name='userPanel'),
    path('Address/',views.address.as_view(),name='address'),
    path('GetAddr/',views.getAddr,name='getAddr'),
    path('removeAddr/',views.deleteAddr,name='removeAddr'),
    # path('checkInfo/',views.,name='checInfo')
    # path('Settings/',views.settings,name='settings'),
    # path('OrderHistory/',views.orderHistory,name='orderHistory'),
]