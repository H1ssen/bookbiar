from django.urls import path
from . import views

app_name = 'shoppingCard'

urlpatterns = [
    path('addItem/',views.addItem.as_view(),name='addItem'),
    path('removeItem/',views.removeItem.as_view(),name='removeItem'),
    path('viewCard/',views.viewCard.as_view(),name='viewCard'),
    path('changeQuantity/',views.changeQuantity.as_view(),name='changeQuantity'),
    path('orderConfirm/<slug:cardId>/',views.orderConfirm.as_view(),name='orderConfirm'),
    path('orderConfirm/',views.orderConfirm.as_view(),name='orderConfirmPost'),
    path('orderPay/',views.orderPay,name='orderPay'),

]