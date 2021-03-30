from django import forms
from django.db.models import fields 
from .models import Comment 

class NewCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
