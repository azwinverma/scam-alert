from django.urls import path
from .views import ScamReportListCreateView, ScamReportDetailView, CommentCreateView, ReactionCreateView

urlpatterns = [
    path('scams/', ScamReportListCreateView.as_view(), name='scam-list-create'),
    path('scams/<int:pk>/', ScamReportDetailView.as_view(), name='scam-detail'),
    path('comments/', CommentCreateView.as_view(), name='comment-create'),
    path('reactions/', ReactionCreateView.as_view(), name='reaction-create'),
]