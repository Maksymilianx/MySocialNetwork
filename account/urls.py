from django.urls import path
from account import views


urlpatterns = [
    path('login/', views.UserLogin.as_view(), name='login'),
]