from django.urls import path
import views


urlpatterns = [
    path('login/', views.UserLogin, name='login'),
]