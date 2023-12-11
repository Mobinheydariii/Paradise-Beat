from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from . import managers



class User(AbstractBaseUser, PermissionsMixin):


    class Types(models.TextChoices):

        SIMPLE_USER = "SIU", "Simple_user" 
        SINGER = "SIN", "Singer" 
        PRODUCER = "PRD", "Producer" 
        MUSICIAN = "MUC", "Musician" 
        SUPORTER = "SPO", "Supporter"

    
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



class SimpleUser(User):

    objects = managers.SimpleUserManager()
    official = managers.OfficialManager()

    class Meta:
        verbose_name = "کاربر ساده"
        verbose_name_plural = "کاربران ساده"

class SimpleUserProfile(models.Model):
    user = models.ForeignKey(SimpleUser,
                             on_delete=models.CASCADE, 
                             verbose_name="کاربر", related_name="simple_user_profile")

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
    
class Singer(User):

    objects = managers.SingerManager()
    official = managers.OfficialManager()


    class Meta:
        ordering = ['status']
        verbose_name = "خواننده"
        verbose_name_plural = "خوانندگان"

    def __str__(self):
        return self.artist_name


class SingerProfile(models.Model):
    singer = models.ForeignKey(Singer,
                                on_delete=models.CASCADE,
                                verbose_name="پروفایل خواننده", related_name="singer_user_profile")

    artistic_name = models.CharField(max_length=200, 
                                     verbose_name="نام هنری", 
                                     unique=True, null=True, blank=True)

    bio = models.TextField(max_length=500, 
                           verbose_name="بیوگرافی", blank=True, null=True)
    
    image = models.ImageField(verbose_name="تصویر پروفایل", 
                              upload_to='singer/image/profile/', blank=True, null=True)

    full_name = models.CharField(verbose_name="نام کامل کاربر",
                                    max_length=200, null=True, blank=True)
    
    def __str__(self):
        return f"{self.singer.username}.....{self.full_name}"


    class Meta:
        verbose_name = "پروفایل خواننده"
        verbose_name_plural = "پروفایل خوانندگان"


class Producer(User):

    objects = managers.ProducerManager()
    official = managers.OfficialManager()


    class Meta:
        ordering = ['status']
        verbose_name = "پرودوسر"
        verbose_name_plural = "پرودوسر ها"

    def __str__(self):
        return self.artist_name
    

class ProducerProfile(models.Model):
    producer = models.ForeignKey(Producer,
                                  on_delete=models.CASCADE,
                                  verbose_name="پرودوسر", related_name="producer_user_profile")

    artistic_name = models.CharField(max_length=200, 
                                     verbose_name="نام هنری", 
                                     unique=True, null=True, blank=True)

    bio = models.TextField(max_length=500, 
                           verbose_name="بیوگرافی", blank=True, null=True)
    
    image = models.ImageField(verbose_name="تصویر پروفایل", 
                              upload_to='singer/image/profile/', blank=True, null=True)

    full_name = models.CharField(verbose_name="نام کامل کاربر",
                                    max_length=200, null=True, blank=True)
    
    def __str__(self):
        return f"{self.producer.username}.....{self.full_name}"


    class Meta:
        verbose_name = "پروفایل پرودوسر"
        verbose_name_plural = "پروفایل پرودوسرها"

class Musician(User):

    objects = managers.MusicianManager()
    official = managers.OfficialManager()

    class Meta:
        ordering = ['status']
        verbose_name = "موزیسین"
        verbose_name_plural = "موزیسین ها"


    def __str__(self):
        return self.artist_name

class MusicianProfile(models.Model):
    musician = models.ForeignKey(Musician, 
                                 on_delete=models.CASCADE,
                                 verbose_name="موزیسین", related_name="musician_user_profile")

    artistic_name = models.CharField(max_length=200, 
                                     verbose_name="نام هنری", 
                                     unique=True, null=True, blank=True)

    bio = models.TextField(max_length=500, 
                           verbose_name="بیوگرافی", blank=True, null=True)
    
    image = models.ImageField(verbose_name="تصویر پروفایل", 
                              upload_to='singer/image/profile/', blank=True, null=True)

    full_name = models.CharField(verbose_name="نام کامل کاربر",
                                    max_length=200, null=True, blank=True)
    
    def __str__(self):
        return f"{self.musician.username}.....{self.full_name}"


    class Meta:
        verbose_name = "پروفایل موزیسین"
        verbose_name_plural = "پروفایل موزیسین ها"


class Supporter(User):

    supporter_id = models.CharField(max_length=20, 
                                    verbose_name="آیدی پشتیبان", unique=True)
    
    supporter_password = models.CharField(max_length=16,
                                          verbose_name="رمز عبور پشتیبان")

    objects = managers.SupporterManager()
    official = managers.OfficialManager()
    

    class Meta:
        ordering = ['supporter_id']
        verbose_name = "پشتیبان"
        verbose_name_plural = "پشتیبان ها"


    def __str__(self):
        return self.supporter_id
    


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