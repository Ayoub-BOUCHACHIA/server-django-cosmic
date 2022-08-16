from django.contrib import admin
from django.urls import path,include
from .views import *

app_name = 'INSERTIONPLATFORM'

urlpatterns = [
    path('', login_user , name="login"),
    path('logout',logout_user, name="logout"),
    path('insertion', main , name="home"),
    path('dataset_generation', generateDataset, name="generation"),
    path('pipline', pipline, name="pipline")
]
