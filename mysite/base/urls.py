from django.urls import path
from . import views

urlpatterns=[
    path('login/',views.loginPage,name='Login'),
    path('logout/',views.logutUser,name='Logout'),
    path('topicsPage/', views.topicsPage, name='Topics'),
    path('recentPage/', views.recentPage, name='Recent'),
    path('profile/<str:pk>',views.userProfile,name='Profile'),
    path('updateprofile/',views.updateProfile,name='Update-Profile'),
    path('register/',views.registerUser,name='Register'),
    path('',views.home,name='home'),
    path('room/<str:pk>',views.room,name="Room"),
    path('create-room/',views.createRoom,name="Create-Room"),
    path('update-room/<str:pk>',views.updateRoom,name="Update-Room"),
    path('delete-room/<str:pk>',views.deleteRoom,name="Delete-Room")
]