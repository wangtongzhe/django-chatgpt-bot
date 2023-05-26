from django.urls import path
from . import views

urlpatterns = [
    path('', views.ChatBotView.as_view(), name="chatbot"),
    path('login', views.LoginView.as_view(), name="login"),
    path('logout', views.logout, name="logout"),
    path('register', views.RegisterView.as_view(), name="register"),
]