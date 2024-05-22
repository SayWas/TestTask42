from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)

from .views import (
    ContractListView,
    ContractDetailView,
    ContractManageUsersView
)

urlpatterns = [
    path('contracts/', ContractListView.as_view(), name='contract-list'),
    path('contracts/<int:pk>/', ContractDetailView.as_view(),
         name='contract-detail'),
    path('contracts/<int:pk>/manage-users/',
         ContractManageUsersView.as_view(), name='contract-manage-users'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
