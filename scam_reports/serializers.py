from rest_framework import serializers
from django.contrib.auth.models import User
from .models import ScamReport, Comment, Reaction


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class CommentSerializer(serializers.ModelSerializer):
    # class Meta:
    #     model = Comment
    #     fields = '__all__'
    commented_by = UserSerializer(read_only=True)  # Include user details

    class Meta:
        model = Comment
        fields = ['id', 'text', 'commented_by', 'created_at','scam_report']

class ReactionSerializer(serializers.ModelSerializer):
    # class Meta:
    #     model = Reaction
    #     fields = '__all__'
    reacted_by = UserSerializer(read_only=True)  # Include user details

    class Meta:
        model = Reaction
        fields = ['id', 'reaction_type', 'reacted_by','scam_report']


class ScamReportSerializer(serializers.ModelSerializer):
     comments = CommentSerializer(many=True, read_only=True)
     reactions = ReactionSerializer(many=True, read_only=True)
     reported_by = serializers.StringRelatedField()

     class Meta:
        model = ScamReport
        fields = [
            'id', 'title', 'description', 'image', 'created_at', 'updated_at',
            'reported_by', 'comments', 'reactions'
        ]

     def validate_title(self, value):
        if not value:
            raise serializers.ValidationError("Title is required.")
        return value

     def validate_description(self, value):
        if not value:
            raise serializers.ValidationError("Description is required.")
        return value
     

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data.get('email', '')
        )
        return user
    
