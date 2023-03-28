from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import SignUpView, AccountActivationView

urlpatterns = [
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('activate/<int:pk>/', AccountActivationView.as_view(), name='activate'),
]