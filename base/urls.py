from django.contrib import admin
from django.urls import path
from django.http import HttpResponse
from . import views

urlpatterns = [ 
    path('login/', views.LoginPage, name = "login"),
    path('logout/', views.LogoutUser, name = "logout"),
    path('register/', views.RegisterUser, name = "register"),

    path('', views.Home, name="home"),
    path('room/<str:pk>/', views.Rooms, name="room"),

    path('create-room/', views.RoomCreate, name="create-room"),
    path('update-room/<str:pk>', views.RoomUpdate, name="update-room"),
    path('delete-room/<str:pk>', views.RoomDelete, name="delete-room"),
]
