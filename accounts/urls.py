from django.contrib.auth.views import LogoutView
from django.urls import path

from accounts.views import RegistrationView, LoginView, ProfileView

urlpatterns = [
    # path('', include('django.contrib.auth.urls')),
    path("logout/", LogoutView.as_view(), name="logout"),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
]
