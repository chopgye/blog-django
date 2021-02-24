from django.urls import path
from . import views       # . is current directory 

# '' its the home for blog path, second arg shows where it is, and
# third arg is the name of this url path in case we want to look it up
urlpatterns = [
    path('', views.home, name='blog-home'),
    path('about/', views.about, name='blog-about')
]