from django.db import models
from django.utils import timezone 
from django.contrib.auth.models import User  #relation between post and user created in django ORM
from django.urls import reverse 
# models are essentionaly objects and we interact with databse using django buil-in ORM
# each class is a table in the database
class Post(models.Model):
    title = models.CharField(max_length =100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now) #no parenthesis to execute, we jsut want value
    author = models.ForeignKey(User, on_delete = models.CASCADE) # 1 to many relation

    def __str__(self):      #special methods, can be called to display said attributes of a given row
        return self.title
    
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})