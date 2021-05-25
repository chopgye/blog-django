# Django Blog

## General Info
This project is my attempt at learning and applying the Django framework and all the other supplementary technologies involved in the process. I wanted to do a project that's simple in concept, therefore I have more freedom to focus all my efforts and complexity on the implementation side. This blog app utilizies MVC framework and handles all the renderings on the server side (SSR). This project is almost purely ran on vanilla Django, with some javascript exceptions such as AJAX calls. 

## Installation
Method 1:
```bash
$ python manage.py migrate
$ python manage.py runserver  
```
\* make sure database exists before migrating

Method 2: Docker 
```bash
$ docker-compose up -d --build
$ docker-compose exec web python manage.py migrate
```

## Features 
* Authentication
* Login/logout 
* Email password reset
* Profile customization 
* Create blog post
  * update 
  * delete 
* Add comments
  * delete
* Upvote / downvote / unvote [post and comments]
* Favorite 
* Sort post by users
* Pagination
  
## Database 
![ERD](https://github.com/chopgye/blog-django/blob/9c59c18b5d2bd58ff7de5a14a1eca0341bb28a7e/Database%20ERD.png?raw=true)
## Technologies
* Python/Django
* PostgresSQL
* HTML
* CSS
* AWS
  * S3 bucket
  * IAM
* Bootstrap
* AJAX calls
* DjangoORM
* Gunicorn
* Pillow
* Docker
* Pipenv
  
## Design Choices
### __Class based views vs function based views__ 
I've predominatly used class based generic views through out this project and only used function based views for very simple tasks. I made this design choice for several reasons. Firstly I wanted to be able to inherit from the multitude of django generic views and mixens. Secondly it made it easy for me to extend and overwrite certain functionalities. Lastly for some of the more general views I wanted the ability to use inhearitance in the future to reduce duplicate code.  

### __Generic Relation__
I used generic relations in my models, becuase the Vote model needed to tie itself to either the Comment model or Post model. However the problem with creating two seperate foriegn key to each model is that by choosing one, the other inevitability becomes null. Therefore generic relations allows for in a sense a polymorphic relation among all the models, where by creating a foreign key to the ContentType allows me to access all the other models.  

### __Abstract model__
I used an abstact model called VoteModel, becuase I realzied the Comment model and Post model shared alot of the same attributes, decorators and functions. So instead of writing duplicate codes I decided to use an abstract model to inherit those shared attributes. In addition, I could also create a generic relation to VoteModel instead of one for Comment model and one for Post model.

### __Custom user__
I wanted to be able to customize user creation process more specifically allow the user to login using email instead of the username. In addition, i wanted to make it so that it was case insensitive. However since i was using django's built in contrib package, i had to create my own customization by extending it. Extending AbstractBaseUser model and the BaseUserManager allowed me to override attributes and functions required for account creation and log in. 

### __AJAX__
Intially when I started this project I wanted to make it strictly a pure Django experience. However, after inplementing the voting system, I realized that in order to display the updated vote count the DOM would have to refresh each time. I've tried many solutions within django to fix it but django didn't allow for updates on single elements. Any changes made required the DOM to refresh completely, therefore I had to use AJAX calls to target specific element within my html.  