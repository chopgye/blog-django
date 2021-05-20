from django.contrib import admin
from .models import Comment, Post, Vote, VoteModel

# Register your models here.
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Vote)
admin.site.register(VoteModel)
