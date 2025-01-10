from rest_framework import serializers
from .models import ScamReport, Comment, Reaction

class ScamReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScamReport
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class ReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reaction
        fields = '__all__'