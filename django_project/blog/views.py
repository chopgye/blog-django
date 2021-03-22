from django.http import request
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView, 
    DetailView, 
    CreateView, 
    UpdateView,
    DeleteView
)
from .models import Post     #the . means modles is located in the sanme directory

# provides inbound HTTP request to django server
def home(request):
    context = {
        'posts': Post.objects.all()   #retrives all the records in Post table from database
    }
    return render(request, 'blog/home.html', context)

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'  #<app>/<model>_<viewtype>.html
    context_object_name = 'posts'   #otherwise object.list is iterated in the template
    ordering = ['-date_posted'] #newest to oldest in the object query
    paginate_by = 5

class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'  #<app>/<model>_<viewtype>.html
    context_object_name = 'posts'   #otherwise object.list is iterated in the template
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

class PostDetailView(DetailView):
    model = Post        #if the naming conevention are maintained this will suffice

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user #add the current user as atuhor before submitting 
        return super().form_valid(form)  #override the parent with author info

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user #add the current user as atuhor before submitting 
        return super().form_valid(form)  #override the parent with author info

    def test_func(self):
        post = self.get_object()  #the current post we're trying to update
        if self.request.user == post.author: #the current user vs author of the post
            return True 
        return False 

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'
    def test_func(self):
        post = self.get_object()  #the current post we're trying to update
        if self.request.user == post.author: #the current user vs author of the post
            return True 
        return False 

def about(request):
    return render(request, 'blog/about.html', {'title':'About'})