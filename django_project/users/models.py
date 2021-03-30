from django.db import models
#from django.contrib.auth.models import User
from PIL import Image
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager 
from django.conf import settings

User = settings.AUTH_USER_MODEL

# processes to override
# create a new user 
# create super user 

class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("Users must have an email adddress.")
        if not username:
            raise ValueError("Users must have a username")
        user = self.model(email=self.normalize_email(email), username=username)
        user.set_password(password)
        user.save(using=self._db)
        
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email), 
            username=username, 
            password=password,
        )
        user.is_admin = True;
        user.is_staff = True;  
        user.is_superuser = True;  
        user.save(using=self._db)
        
        return user   
class Account(AbstractBaseUser):
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username = models.CharField(max_length=30, unique=True)
    data_joined = models.DateTimeField(verbose_name="data_joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'        #used for login
    REQUIRED_FIELDS = ['username']      #still required even tho its not used

    objects = MyAccountManager()  #set the account manager to the custom user model 

    def __str__(self):
        return f'{self.username}'
    
    def has_perm(self, perm, obj=None):     #overriding this method from baseuser to manage permissions 
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    # def save(self, *args, **kwargs): #overwite the save method 
    #     super().save(*args, **kwargs) #run the parent method built in django

    #     img = Image.open(self.image.path)

    #     if img.height > 300 or img.width > 300:
    #         output_size = (300, 300)
    #         img.thumbnail(output_size)
    #         img.save(self.image.path)
  