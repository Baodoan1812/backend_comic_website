from django.urls import path
from .views import UserCreateView, UserDeleteView, UserInfoView
from .views_auth import CustomTokenObtainPairView

urlpatterns = [
    path('create/', UserCreateView.as_view(), name='user-create'),
    path('delete/<int:id>/', UserDeleteView.as_view(), name='user-delete'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('me/', UserInfoView.as_view(), name='user_info'),
]
