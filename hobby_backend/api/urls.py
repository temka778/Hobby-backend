from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from api.views import SignupView, CustomTokenObtainPairView, LogoutView, UserDetailView, home


urlpatterns = [
    path("signup/", SignupView.as_view(), name="signup"),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("users/<str:lookup>/", UserDetailView.as_view(), name="user-detail"),
    path('', home, name='home'),
]