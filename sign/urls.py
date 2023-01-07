from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from sign.views import BaseRegisterView, login_view, verify_view

urlpatterns = [
    path('login/', login_view, name='login'),
    path('verify/', verify_view, name='verify'),
    path('logout/', 
        LogoutView.as_view(template_name = 'sign/logout.html'),
        name='logout'),
    path('signup/', 
        BaseRegisterView.as_view(template_name = 'sign/signup.html'), 
        name='signup'),
]