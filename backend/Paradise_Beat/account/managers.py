from django.db.models import Manager
from django.contrib.auth.models import BaseUserManager
from . import models




class OfficialManager(Manager):
    def get_queryset(self, *args, **kwargs):
        # Return queryset of only oficial Users
        return super().get_queryset(*args, **kwargs).filter(status=models.User.UserStatus.OFFICIAL)
    
class UserManager(BaseUserManager):
    # Method to create user with provided credentials
    def create_user(self, username, email , phone, type, password=None): 
        email = email.lower()
        user = self.model( 
            username = username,
            email = email,
            phone = phone,
            type = type,
        ) 
        user.set_password(password) 
        user.save(using = self._db) 
        return user 

    # Method to create superuser with provided credentials
    def create_superuser(self, username, email, phone, password=None):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            phone=phone,
            type="SIM",
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