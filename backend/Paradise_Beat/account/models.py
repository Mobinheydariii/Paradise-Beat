from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from . import managers



class User(AbstractBaseUser, PermissionsMixin):


    class Types(models.TextChoices):

        SIMPLE_USER = "SIM", "Simple_user"
        SINGER = "SIN", "Singer"
        PRODUCER = "PRD", "Producer"
        MUSICIAN = "MUC", "Musician"

    
    class UserStatus(models.TextChoices):
        
        OFFICIAL = "OFL", "Official"
        UN_OFFICIAL = "UFL", "Un_Official"


    type = models.CharField(
        max_length=3, 
        choices=Types.choices,
    )

    status = models.CharField(
        max_length=3,
        verbose_name="وضعیت کاربر", 
        choices=UserStatus.choices, 
        default=UserStatus.UN_OFFICIAL,
    )
    
    phone = models.CharField(verbose_name="شماره",
                             max_length=11, unique=True)
    
    email = models.EmailField(verbose_name="ایمیل", unique=True)
    
    username = models.CharField(verbose_name="نام کاربر", 
                                 max_length=40, unique=True)
    
    slug = models.SlugField(verbose_name="اسلاگ پروفایل", 
                             max_length=40, unique=True)
    
    joined = models.DateField(auto_now_add=True,)

    is_active = models.BooleanField(verbose_name="فعال", default=True)
    is_admin = models.BooleanField(verbose_name="ادمین", default=False)

    
    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = ['email', "username"]

    objects = managers.UserManager()
    simple_user = managers.SimpleUserManager()
    singer = managers.SingerManager()
    producer = managers.ProducerManager()
    musician = managers.MusicianManager()
    supporter = managers.SupporterManager()
    official = managers.OfficialManager()



    class Meta:
        ordering = ['type']
        verbose_name = "کاربر"
        verbose_name_plural = "کاربر ها"


    def __str__(self):
        return self.username
    

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

class UserProfile(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE, 
                             verbose_name="کاربر", related_name="user_profile")
    
    artistic_name = models.CharField(max_length=200, 
                                     verbose_name="نام هنری", 
                                     unique=True, null=True, blank=True)

    bio = models.TextField(max_length=500, 
                           verbose_name="بیوگرافی", blank=True, null=True)
    
    image = models.ImageField(verbose_name="تصویر پروفایل", 
                              upload_to='users/', blank=True, null=True)

    full_name = models.CharField(verbose_name="نام کامل کاربر",
                                    max_length=200, blank=True, null=True)
    
    def __str__(self):
        return f"{self.user.username}.....{self.full_name}"


    class Meta:
        verbose_name = "پروفایل کاربر ساده"
        verbose_name_plural = "پروفایل کاربران ساده" 


class UserSocialMedia(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             verbose_name="کاربر", related_name="user_social_media")

    instagram = models.CharField(max_length=200, 
                                 unique=True, null=True, blank=True)

    facebook = models.CharField(max_length=200, 
                                 unique=True, null=True, blank=True)
    
    youtube = models.CharField(max_length=200, 
                                 unique=True, null=True, blank=True)
    
    sound_cloud = models.CharField(max_length=200, 
                                    unique=True, null=True, blank=True)
    
    tik_tok = models.CharField(max_length=200, 
                                unique=True, null=True, blank=True)
    

    def __str__(self):
        return self.user.username


class UserFollower(models.Model):
    user = models.ForeignKey(User, 
                             on_delete=models.CASCADE, 
                             verbose_name="کاربر", related_name="user_followers")
    
    follower_user = models.ManyToManyField(User,
                                            related_name='follower_user', blank=True)

    qountity = models.IntegerField(default=0)

    
    class Meta:
        verbose_name = "فالور"
        verbose_name_plural = "فالور ها"

    
    def __str__(self):
        return f'{self.user.username}-{self.qountity}'
    

    def add_follower(self, user):
        if user not in self.follower_user.all():
            self.follower_user.add(user)
            self.qountity += 1
            self.save()


    def remove_follower(self, user):
        if user in self.follower_user.all():
            self.follower_user.remove(user)
            self.qountity -= 1
            self.save()


class UserFollowing(models.Model):
    user = models.ForeignKey(User, 
                             on_delete=models.CASCADE, 
                             verbose_name="کاربر", related_name="user_followings")
    
    following_user = models.ManyToManyField(User, 
                                             related_name='following_user', blank=True)

    qountity = models.IntegerField(default=0)

    
    class Meta:
        verbose_name = "دنبال کننده"
        verbose_name_plural = "دنبال کنندگان"
    

    def __str__(self):
        return f'{self.user.username}-{self.qountity}'
    
    
    def add_following(self, user):
        if user not in self.following_user.all():
            self.following_user.add(user)
            self.qountity += 1
            self.save()


    def remove_following(self, user):
        if user in self.following_user.all():
            self.following_user.remove(user)
            self.qountity -= 1
            self.save()


class Otp(models.Model):
    phone = models.CharField(verbose_name="شماره تلقن", max_length=11)

    email = models.EmailField(verbose_name="ایمیل")

    username = models.CharField(verbose_name="نام کربری", max_length=20)

    password = models.CharField(max_length=16)

    password2 = models.CharField(max_length=16)

    token = models.CharField(max_length=200)

    code = models.CharField(max_length=6)

    type = models.CharField(max_length=3,
                             choices=User.Types.choices,
                             default=User.Types.SIMPLE_USER)
    
    is_used = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.phone}....{self.username}"