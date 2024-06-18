

from django.contrib import admin
from django.urls import path ,re_path
from .views import *




urlpatterns = [
   
    path('signup/',index ,name ="signup"),
    
    path('total_item/',total_item ,name ='total_item'),
    path('login/',login,name = 'login'),
    path('logout/',logout,name ='logout'),

    path('data/',data,name ='data'),
    path('server/',server_side,name ='server'),
    path('server2/',server2 ,name ='server2'),
    path('data_detail/<int:id>/',data_detail ,name ='data_details'),
    path('upload_data/', upload_data, name='upload_data'),
    path('masters/',masters,name ='masters'),
    path('data_masters/',data_masters,name ='data_masters'),
    path('update_data/',update_data,name ="update_data"),
    path('add_data/',add_data,name= "add_data"),
    
]

