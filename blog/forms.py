from django import forms
from django.db.models import fields
from django.forms import widgets 
from .models import Comment, Vote 

class NewCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

class VoteForm(forms.ModelForm):
    class Meta:
        model = Vote
        fields = ['type_of_vote']
       # widgets = {
       #     'type_of_vote': forms.Select(attrs={'onchange': 'submit();'})
       # }