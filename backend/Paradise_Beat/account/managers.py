from django.db.models import Manager
from django.contrib.auth.models import BaseUserManager
from . import models






class OfficialManager(Manager):
    def get_queryset(self, *args, **kwargs):
        # Return queryset of only oficial Users
        return super().get_queryset(*args, **kwargs).filter(status=models.User.UserStatus.OFFICIAL)
    
class UserManager(BaseUserManager):
    # Method to create user with provided credentials
    def create_user(self , username, email , phone, password = None): 
        # Validate username
        if not username or len(username) <= 0 :
            raise ValueError("Users must have a valid username")
        # Validate phone number
        if not phone or len(phone) <= 0 :
            raise ValueError('Phone number is required ')
        # Validate email
        if not email or len(email) <= 0 :  
            raise ValueError("Email field is required !") 
        # Validate password
        if not password or len(password) < 8 :
            raise ValueError("Password should be at least 8 characters long ")
        
        # Create user
        email = email.lower() 
        user = self.model( 
            username = username,
            email = email,
            phone = phone
        ) 
        user.set_password(password) 
        user.save(using = self._db) 
        return user 

    # Method to create superuser with provided credentials
    def create_superuser(self, username, email, phone, password=None):
        # Validate username
        if not username or len(username) <= 0 :
            raise ValueError("Users must have a valid username")
        # Validate phone number
        if not phone or len(phone) <= 0 :
            raise ValueError('Phone number is required ')
        # Validate email
        if not email or len(email) <= 0 :  
            raise ValueError("Email field is required !") 
        # Validate password
        if not password or len(password) < 8 :
            raise ValueError("Password should be at least 8 characters long ")
        
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            phone=phone,
            password=password
        )
        user.is_admin = True
        user.save(using=self._db)
        return user
    


class SimpleUserManager(Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=models.User.Types.SIMPLE_USER)
    

class SingerManager(Manager):
    # get singer queryset
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=models.User.Types.SINGER)
    

class ProducerManager(Manager):
    # Method to get queryset for producer users
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=models.User.Types.PRODUCER)


class MusicianManager(Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=models.User.Types.MUSICIAN)


class SupporterManager(Manager):
    # Method to filter queryset by user type
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=models.User.Types.SUPORTER)