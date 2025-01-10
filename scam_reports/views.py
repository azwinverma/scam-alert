from django.shortcuts import get_object_or_404
from rest_framework import generics
from .models import ScamReport, Comment, Reaction
from .serializers import ScamReportSerializer, CommentSerializer, ReactionSerializer
from .forms import CommentForm, ReactionForm

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

def add_comment(request, pk):
    scam_report = get_object_or_404(ScamReport, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.scam_report = scam_report
            comment.user = request.user
            comment.save()
            return redirect('admin:scam_report_change', pk=scam_report.pk)
    else:
        form = CommentForm()
    return redirect('admin:scam_report_change', pk=scam_report.pk)

def add_reaction(request, pk):
    scam_report = get_object_or_404(ScamReport, pk=pk)
    if request.method == 'POST':
        form = ReactionForm(request.POST)
        if form.is_valid():
            reaction = form.save(commit=False)
            reaction.scam_report = scam_report
            reaction.user = request.user
            reaction.save()
            return redirect('admin:scam_report_change', pk=scam_report.pk)
    else:
        form = ReactionForm()
    return redirect('admin:scam_report_change', pk=scam_report.pk)