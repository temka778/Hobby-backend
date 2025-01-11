from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from api.views import SignupView, LogoutView, UserDetailView, CurrentUserView, home


urlpatterns = [
    path("signup/", SignupView.as_view(), name="signup"),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("logout/", LogoutView.as_view(), name="logout"),
    path('users/me/', CurrentUserView.as_view(), name='current_user'),
    path("users/<int:id>/", UserDetailView.as_view(), name="user-by-id"),
    path("users/<str:username>/", UserDetailView.as_view(), name="user-by-username"),
    path('', home, name='home'),
]