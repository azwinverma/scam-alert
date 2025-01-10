# forms.py
from django import forms
from .models import Comment, Reaction

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

class ReactionForm(forms.ModelForm):
    class Meta:
        model = Reaction
        fields = ['reaction_type']
