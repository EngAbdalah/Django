# myAuth/urls.py
from django.urls import path
# from .views import login_view, register_view, logout_view
from . import views 


app_name = 'myauth'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
]
