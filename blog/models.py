from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import TextField
from django.utils import timezone 
#from django.contrib.auth.models import User  #relation between post and user created in django ORM
from django.urls import reverse
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType


User = settings.AUTH_USER_MODEL
# models are essentionaly objects and we interact with databse using django buil-in ORM
# each class is a table in the database
class Vote(models.Model):
    VOTE_CHOICES = (
        ('U','Upvote'),
        ('D','Downvote'),
        ('F','Favorite')
    )

    #basic implemntation for generic relations
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_submission = models.DateTimeField(default=timezone.now) 
    type_of_vote = models.CharField(max_length=1, choices=VOTE_CHOICES)

    def __str__(self):
        return f'voter:{self.author} post/comment: {self.content_object} type: {self.type_of_vote}'

class VoteModel(models.Model):
    votes = GenericRelation(Vote)
    class meta:
        abstract = True
    
    # alternative: implment how user can interact with the vote table, current this is implemented in the views 
    def upvote(self, User):
        Vote.objects.create(content_object=self, type_of_vote='U', author=User.request.user)
        self.num_upvotes += 1

    def downvote(self, User):
        Vote.objects.create(content_object=self, type_of_vote='D', author=User.request.user)
        self.num_downvotes += 1
   
    def save(self, *args, **kwargs):
        super(VoteModel, self).save(*args, **kwargs)

    @property
    def number_of_votes(self):
        return self.votes.filter(type_of_vote='U').count() - self.votes.filter(type_of_vote='D').count()

    @property
    def content_type(self): 
        return ContentType.objects.get_for_model(self).model

    @property
    def num_upvotes(self):
        return self.votes.filter(type_of_vote='U').count()
    
    @property
    def num_downvotes(self):
        return self.votes.filter(type_of_vote='D').count()
    
    @property 
    def num_favorites(self):
        return self.votes.filter(type_of_vote='F').count()
    
class Post(VoteModel):
    title = models.CharField(max_length =100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now) #no parenthesis to execute, we jsut want value
    author = models.ForeignKey(User, on_delete = models.CASCADE) # 1 to many relation
 #   votes = GenericRelation(Vote)

    def __str__(self):      #special methods, can be called to display said attributes of a given row
        return f'title: {self.title}'
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})
    
    def get_absolute_url_home(self):
        return reverse('blog-home')
   
    def get_vote_url(self):
        return reverse('post-vote', kwargs={'pk': self.pk})
    
    @property
    def number_of_comments(self):
        return Comment.objects.filter(parent_post=self).count()
    
    @property
    def is_upvoted(self):
        if Vote.objects.filter(object_id = self.id, type_of_vote = 'U'):
            isUpvoted = True
        else:
            isUpvoted = False 

        return isUpvoted

    @property
    def is_downvoted(self):
        if Vote.objects.filter(object_id = self.id, type_of_vote = 'D'):
            isDownvoted = True
        else:
            isDownvoted = False 

        return isDownvoted

    @property
    def is_favorited(self):
        if Vote.objects.filter(object_id = self.id, type_of_vote = 'F'):
            isFavorited = True
        else:
            isFavorited = False 

        return isFavorited
    
class Comment(VoteModel):
    parent_post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=CASCADE)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
 #   votes = GenericRelation(Vote)

    def __str__(self):
        return f'author: {self.author} content: {self.content[:20]}'

