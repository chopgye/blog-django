from django.contrib.contenttypes.models import ContentType
from django.db.models import query
from django.db.models.query_utils import Q
from django.http import request, response
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
#from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView, 
    DetailView, 
    CreateView, 
    UpdateView,
    DeleteView
)
from django.views.generic.base import RedirectView
from .models import Post, VoteModel     #the . means modles is located in the sanme directory

from users.models import Account as User
from .models import Comment, Vote
from .forms import NewCommentForm, VoteForm
from django.http import HttpResponse
import json
from django.core import serializers
from django.template.loader import render_to_string


# provides inbound HTTP request to django server
def home(request):
    context = {
        'posts': Post.objects.all(),   #retrives all the records in Post table from database
    }
    return render(request, 'blog/home.html', context)

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'  #<app>/<model>_<viewtype>.html
    context_object_name = 'posts'   #otherwise object.list is iterated in the template
    ordering = ['-date_posted'] #newest to oldest in the object 
        
class PostLikeToggle(RedirectView):
    model = Post
    template_name = 'blog/home.html'  #<app>/<model>_<viewtype>.html
    context_object_name = 'posts'   #otherwise object.list is iterated in the template


    def post(self, request, *args, **kwargs):
        if self.request.POST.get("content_type","") == 'post':  #refer to property decorator in models 
            model_type = get_object_or_404(Post, id=self.request.POST.get("id", ""))
        elif self.request.POST.get("content_type","") == 'comment':
            model_type = get_object_or_404(Comment, id=self.request.POST.get("id", ""))

        vote_choice = self.request.POST.get("vote_type", "")

        flag = False           # if vote exist (false = doesn't exist)

        #clear favroites by the current user on the current post, if flag is true don't creat new favorite
        # favroite logic seperated from vote logic to avoid collision where vote instance exist but type of vote = F leading to 404
        if Vote.objects.filter(author = self.request.user, object_id = model_type.id, type_of_vote = 'F'):
           
            if vote_choice == 'post_favorited':
                curr_vote = get_object_or_404(Vote, type_of_vote = 'F', object_id = model_type.id, author = self.request.user)
                curr_vote.delete()
                flag = True
        
        #needs to catch both 'U' and 'D' conditions          
        if (Vote.objects.filter(object_id = model_type.id, author = self.request.user, type_of_vote = 'U')) or (Vote.objects.filter(object_id = model_type.id, author = self.request.user, type_of_vote = 'D')):
            print(self.request.user.id)

           # flag means that same type of vote currently exists and is therefore deleted, no new additions 
           # print(f'current vote: {curr_vote}')
            if vote_choice == 'post_upvoted':
                
                #we know an upvote or downvote exist, try one at a time, one of them will succeed and the other will throw 404
                #needs to exist after post_voted, because otherwise 
                try:    
                    curr_vote = get_object_or_404(Vote, type_of_vote = 'U', author = self.request.user, object_id = model_type.id )
                except:
                    curr_vote = get_object_or_404(Vote, type_of_vote = 'D', author = self.request.user, object_id = model_type.id )

                if curr_vote.type_of_vote == 'U':
                    curr_vote.delete()
                    flag = True
                else:
                    curr_vote.delete()               #deletes polar votes i.e if post is upvoted but a downvote exists 
 
            if vote_choice == 'post_downvoted':
                try:    
                    curr_vote = get_object_or_404(Vote, type_of_vote = 'U', author = self.request.user, object_id = model_type.id )
                except:
                    curr_vote = get_object_or_404(Vote, type_of_vote = 'D', author = self.request.user, object_id = model_type.id )
                if curr_vote.type_of_vote == 'D':
                    curr_vote.delete()
                    flag = True
                else:
                    curr_vote.delete()

        #flag = false: means no existing upvotes in database, therefore create a new one
        if vote_choice == 'post_upvoted' and flag == False:             
            new_vote = Vote(type_of_vote='U',
                                author=self.request.user,
                                content_object=model_type)
            new_vote.save()
            model_type.save()


        #flag = false: means there is no existing downvotes in the database 
        # delete any potentional upvotes and a new downvote
        if vote_choice == 'post_downvoted' and flag == False:
            new_vote = Vote(type_of_vote='D',
                                author=self.request.user,
                                content_object=model_type)
            new_vote.save()
            model_type.save()

        #flag = false: means there is no existing downvotes in the database 
        # delete any potentional upvotes and a new downvote
        if vote_choice == 'post_favorited' and flag == False:
            new_vote = Vote(type_of_vote='F',
                                author=self.request.user,
                                content_object=model_type)
            new_vote.save()
            model_type.save()

        if Vote.objects.filter(author = self.request.user, object_id = model_type.id, type_of_vote = 'U'):
            isUpvoted = True
        else:
            isUpvoted = False 

        if Vote.objects.filter(author = self.request.user, object_id = model_type.id, type_of_vote = 'D'):
            isDownvoted = True
        else:
            isDownvoted = False
    
        if Vote.objects.filter(author = self.request.user, object_id = model_type.id, type_of_vote = 'F'):
            isFavorited = True
        else:
            isFavorited = False
        
        if request.method == 'POST' and request.is_ajax():
                json_dict = {
                    'vote_count': model_type.number_of_votes,
                    'post_upvotes': model_type.num_upvotes,    
                    'post_downvotes':model_type.num_downvotes,
                    'post_favorites':model_type.num_favorites,
                    'is_upvoted': isUpvoted,
                    'is_downvoted': isDownvoted,
                    'is_favorited': isFavorited,
                }
                return JsonResponse(json_dict, safe=False)
    
        return JsonResponse({"Error": ""}, status=400)

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

    def get_context_data(self, **kwargs):   #override this method, to pass more context than the original implemenation
        context = super().get_context_data(**kwargs)   #call base implementaion to get the base context

        comments_connected = Comment.objects.filter(parent_post=self.get_object()).order_by('-date_posted')
        context['comments'] = comments_connected
        
        if self.request.user.is_authenticated:
            context['comment_form'] = NewCommentForm(instance = self.request.user)
        return context

    #need a post method to retrive the context back from our forms and to the detailview
    def post(self, request, *args, **kwargs):
        new_comment = Comment(content=request.POST.get('content'),
                                  author=self.request.user,
                                  parent_post=self.get_object())
        new_comment.save()
        return self.get(self, request, *args, **kwargs)

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