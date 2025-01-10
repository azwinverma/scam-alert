from rest_framework import generics
from .models import ScamReport, Comment, Reaction
from .serializers import ScamReportSerializer, CommentSerializer, ReactionSerializer

class ScamReportListCreateView(generics.ListCreateAPIView):
    queryset = ScamReport.objects.all()
    serializer_class = ScamReportSerializer

class ScamReportDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ScamReport.objects.all()
    serializer_class = ScamReportSerializer

class CommentCreateView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class ReactionCreateView(generics.CreateAPIView):
    queryset = Reaction.objects.all()
    serializer_class = ReactionSerializer