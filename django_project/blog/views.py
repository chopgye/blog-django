from django.shortcuts import render

# dummy data
posts = [
    {
        'author': 'dorjeeC',
        'title': 'post 1',
        'content': 'first content',
        'date_posted': 'feb 18, 2021'
    },
    {
        'author': 'dhargyeT',
        'title': 'post 2',
        'content': 'second content',
        'date_posted': 'feb 19, 2021'
    },
]

# provides inbound HTTP request to django server
def home(request):
    context = {
        'posts':posts
    }
    return render(request, 'blog/home.html', context)

def about(request):
    return render(request, 'blog/about.html', {'title':'About'})