from django.urls import path
from .views import ScamReportListCreateView, ScamReportDetailView, CommentCreateView, ReactionCreateView
from . import views

urlpatterns = [
    path('scams/', ScamReportListCreateView.as_view(), name='scam-list-create'),
    path('scams/<int:pk>/', ScamReportDetailView.as_view(), name='scam-detail'),
    # path('comments/', CommentCreateView.as_view(), name='comment-create'),
    # path('reactions/', ReactionCreateView.as_view(), name='reaction-create'),
     path('scam_report/<int:pk>/add_comment/', views.add_comment, name='add_comment'),
    path('scam_report/<int:pk>/add_reaction/', views.add_reaction, name='add_reaction'),
]