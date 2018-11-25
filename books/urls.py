from django.urls import path
from . import views
from .models import Categori

app_name='books'

urlpatterns = [
    path('',views.Home.as_view(),name='home'),
    path('Home/',views.Home.as_view(),name='Home'),
    path('<int:typeId>/<int:indexId>/<str:name>',views.Index.as_view(),name="index"),
    path('product/<int:pId>/<str:name>',views.Detail.as_view(),name="detail")
    # path('index/',views.index,name='index')
]