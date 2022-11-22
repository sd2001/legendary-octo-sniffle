from django.urls import path
from .views import AuthService, UserService

urlpatterns = [
    path('authenticate', AuthService.login_user, name="Login User"),
    path('create_user', UserService.create_user, name="Create User"),
    path('details', UserService.get_user, name="Get Individual user details")
    
]
