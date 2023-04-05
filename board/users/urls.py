from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import SignUpView, AccountActivationView, ChangePasswordView, EditProfileView, ProfileView

urlpatterns = [
    path('login/', LoginView.as_view(template_name='users/signup.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('activate/<int:pk>/', AccountActivationView.as_view(), name='activate'),
    path('password-change/', ChangePasswordView.as_view(), name='password_change'),
    path('profile/edit/', EditProfileView.as_view(), name='profile_edit'),
]
