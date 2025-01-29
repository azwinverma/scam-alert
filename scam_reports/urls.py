from django.urls import path
from .views import ScamReportListCreateView, ScamReportDetailView, CommentCreateView, ReactionCreateView, addScamReport
from . import views
from .views import UserRegistrationView,CustomTokenObtainPairView
from .views import UserLoginView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('scams/', ScamReportListCreateView.as_view(), name='scam-list'),
        path('scams/add/', addScamReport, name='addScamReport'),

    path('scams/<int:pk>/', ScamReportDetailView.as_view(), name='scam-detail'),
    # path('comments/', CommentCreateView.as_view(), name='comment-create'),
    # path('reactions/', ReactionCreateView.as_view(), name='reaction-create'),
     path('scam_report/<int:pk>/add_comment/', CommentCreateView.as_view(), name='add_comment'),
    path('scam_report/<int:pk>/add_reaction/', ReactionCreateView.as_view(), name='add_reaction'),
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token-obtain-pair'),  # Login to get tokens
      path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),  # Refresh access 

]