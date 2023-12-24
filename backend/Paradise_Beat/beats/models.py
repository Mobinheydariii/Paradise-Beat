from django.db import models
from account.models import User
from . import managers


class Category(models.Model):
    # Category name, 100 characters maximum
    name = models.CharField(max_length=100, verbose_name="نام دسته بندی")
    
    # Category slug, 100 characters maximum, unique
    slug = models.SlugField(max_length=100, verbose_name="اسلاگ دسته بندی", unique=True)
    
    # Category image, upload to "categories/images/" directory
    image = models.ImageField(verbose_name="تصویر دسته بندی", upload_to="categories/images/")

    # Return category name when printed
    def __str__(self):
        return self.name

    # Define meta information for category model
    class Meta:
        verbose_name = "دسته بندی" # Category, singular
        verbose_name_plural = "دسته بندی ها" # Categories, plural
    

class Tag(models.Model):
    # name of the tag
    name = models.CharField(max_length=100, verbose_name="نام برچسب")

    # slug for tag (unique identifier)
    slug = models.SlugField(max_length=100, verbose_name="اسلاگ برچسب", unique=True)

    # return name as string representation of tag
    def __str__(self):
        return self.name

    # define metadata for tag model
    class Meta:
        # human-readable name of tag model
        verbose_name = "برچسب"

        # human-readable name of tag model (plural)
        verbose_name_plural = "برچسب ها"


class Beat(models.Model):

    class MainStatus(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLIC = 'PU', 'Public'
        PRIVATE = 'PR', 'Private'

    class Status(models.TextChoices):
        ACCEPTED = 'َAC', 'Accepted'
        REJECTED = 'RJ', 'Rejected'
        CHECKING = 'CH', 'Checking'
    

    # Category for this Beat
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="دسته بندی")

    # Tags for this Beat
    tags = models.ManyToManyField(Tag, verbose_name="برچسب ها", blank=True)

    # Producer or the musician 
    producer = models.ForeignKey(User,
                                 on_delete=models.CASCADE,
                                 related_name="producer", verbose_name="پرودوسر")
    
    # Represents the title of the Beat
    title = models.CharField(max_length=200, verbose_name="تایتل بیت", unique=True)

    # Represents the URL slug for the Beat
    slug = models.SlugField(max_length=200, verbose_name="اسلاگ(url)", unique=True)

    # Represents the beats per minute (BPM) of the Beat
    bpm = models.BigIntegerField(blank=True, null=True)

    # Represents the musical keys of the Beat
    keys = models.CharField(max_length=20, blank=True, null=True)

    # Represents the image of the Beat
    image = models.ImageField(verbose_name="تصویر بیت", upload_to="Beats/images/image/", blank=True, null=True)

    # Represents the free mp3 file of the Beat
    mp3_free = models.FileField(verbose_name="mp3 رایگان", upload_to='Beats/files/mp3/free/', blank=True, null=True)

    # Represents the premium mp3 file of the Beat
    mp3_no_tag_in = models.FileField(verbose_name="pm3 پولی", upload_to='Beats/files/mp3/no_tag/', blank=True, null=True)

    # Represents the wav file of the Beat
    wav = models.FileField(verbose_name="فایل wav", upload_to='Beats/files/wav/', blank=True, null=True)

    # Represents the published_status of the Beat
    main_status = models.CharField(
        max_length=2,
        choices=MainStatus.choices,
        default=MainStatus.DRAFT
    )

    # Represents the status of the Beat
    status = models.CharField(
        max_length=3, 
        choices=Status.choices, 
        default=Status.CHECKING
    )

    # Represents the total plays of the Beat
    plays = models.IntegerField(verbose_name="تعداد پلی", default=0)

    # Represents the total likes of the Beat
    likes = models.IntegerField(verbose_name="تعداد لایک", default=0)

    # Represents the total dislikes of the Beat
    dislikes = models.IntegerField(verbose_name="تعداد dislike ها", default=0)

    # Represents the total comments of the Beat
    comments = models.IntegerField(verbose_name="تعداد کامنت ها", default=0)

    # Represents the publish date of the Beat
    publish = models.DateField(verbose_name="زمان انتشار", blank=True, null=True)

    is_published = models.BooleanField(verbose_name="پابلیک شده", default=True)

    # Represents the created date of the Beat
    created = models.DateTimeField(auto_now_add=True)

    # Represents the updated date of the Beat
    updated = models.DateTimeField(auto_now=True)

    permium_licence_status = models.BooleanField(verbose_name="وضعیت اشتراک پرمیوم", default=True)

    basic_licence_status = models.BooleanField(verbose_name="وضعیت اشتراک بیسیک", default=True)

    has_active_licence = models.BooleanField(default=True)
    # Managers for the Beat model
    objects = models.Manager()
    accepted = managers.AcceptedManager()
    rejected = managers.RejectedManager()
    checking = managers.CheckingManager()
    public = managers.PublicManager()
    drafts = managers.DraftManager()
    private = managers.PrivateManager()

    class Meta:
        verbose_name = "بیت"
        verbose_name_plural = "بیت ها"
        ordering = ['-publish']

    def __str__(self):
        return self.title




class PermiumBeatLicence(models.Model):
    class PermiumLicenceStatus(models.TextChoices):
        ACTIVE = 'AC', 'Active'
        EXPIRED = 'EX', 'Expired'
    

    beat = models.ForeignKey(Beat, 
                             on_delete=models.CASCADE, 
                             verbose_name="بیت", related_name="beat_permium_lisence")
    
    price = models.BigIntegerField(verbose_name="قیمت", default=500000)

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL, null=True,
        verbose_name="خریدار", related_name="user_permium_licence_owner"
    )

    status = models.CharField(
        max_length=2,
        choices = PermiumLicenceStatus.choices,
        default = PermiumLicenceStatus.ACTIVE
    )


class BasicBeatLicence(models.Model):
    class BasicLicenceStatus(models.TextChoices):
        ACTIVE = 'AC', 'Active'
        EXPIRED = 'EX', 'Expired'
    

    beat = models.ForeignKey(Beat, 
                             on_delete=models.CASCADE, 
                             verbose_name="بیت", related_name="beat_basic_lisence")
    
    price = models.BigIntegerField(verbose_name="قیمت", default=300000)

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL, null=True,
        verbose_name="خریدار", related_name="user_basic_licence_owner"
    )

    status = models.CharField(
        max_length=2,
        choices = BasicLicenceStatus.choices,
        default = BasicLicenceStatus.ACTIVE
    )


class Comment(models.Model):
    
    beat = models.ForeignKey(Beat, 
                            on_delete=models.CASCADE,
                            related_name="Beat_comments", verbose_name="کامنت های بیت")
    
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE, 
                             related_name="user_comment", verbose_name="کامنت کاربر")
    
    comment = models.TextField(verbose_name="کامنت")

    updated = models.DateTimeField(verbose_name="آخرین آپدیت", auto_now=True)
    created = models.DateTimeField(verbose_name="زمان کامنت", auto_now_add=True)

    class Meta:
        ordering = ["created"]
        verbose_name = "کامنت"
        verbose_name_plural = "کامنت ها"

    
    def __str__(self):
        return f'{self.bit.title}---{self.user.user_name}'


class BeatLike(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name="user_beat_likes")
    
    beat = models.ForeignKey(Beat,
                             on_delete=models.CASCADE, 
                             related_name="beat_likes")
    is_liked = models.BooleanField(default=False)



class BeatDisLike(models.Model):
    user = models.OneToOneField(User,
                                on_delete=models.PROTECT,
                                related_name='user_beat_dislike')
    
    beat = models.ForeignKey(Beat,
                             on_delete=models.CASCADE, 
                             related_name="beat_dislike")
    
    is_disliked = models.BooleanField(default=False)
