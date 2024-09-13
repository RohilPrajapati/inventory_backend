from django.urls import path
from .views import HelloWorldAPIView,LoginView,UserListView,UserRegistration, RoleView,RoleDetailView,ChangePasswordView
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('helloWorld/', HelloWorldAPIView.as_view(),name='hello_world_api'),
    path('login/', LoginView.as_view(), name='login'),
    path('', UserListView.as_view(), name='user_list'),
    path('registration/', UserRegistration.as_view(), name='registration'),
    path('role/', RoleView.as_view(), name='role'),
    path('role/<int:pk>/', RoleDetailView.as_view(), name='role_detail_view'),
    # third party url
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('password/change/', ChangePasswordView.as_view(), name='change_password'),
]