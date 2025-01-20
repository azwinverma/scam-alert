from rest_framework import serializers
from .models import ScamReport, Comment, Reaction

class ScamReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScamReport
        fields = '__all__'

    def validate_title(self, value):
        if not value:
            raise serializers.ValidationError("Title is required.")
        return value

    def validate_description(self, value):
        if not value:
            raise serializers.ValidationError("Description is required.")
        return value

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class ReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reaction
        fields = '__all__'