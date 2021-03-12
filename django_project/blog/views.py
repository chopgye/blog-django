from django.shortcuts import render
from .models import Post     #the . means modles is located in the sanme directory

# provides inbound HTTP request to django server
def home(request):
    context = {
        'posts': Post.objects.all()   #retrives all the records in Post table from database
    }
    return render(request, 'blog/home.html', context)

def about(request):
    return render(request, 'blog/about.html', {'title':'About'})