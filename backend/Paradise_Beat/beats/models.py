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

    class Publish(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PU', 'Published'


    class Status(models.TextChoices):
        ACCEPTED = 'َAC', 'Accepted'
        REJECTED = 'RJ', 'Rejected'
        CHECKIND = 'CH', 'Checking'
    

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
    bpm = models.BigIntegerField()

    # Represents the musical keys of the Beat
    keys = models.CharField(max_length=20)

    # Represents the image of the Beat
    image = models.ImageField(verbose_name="تصویر بیت", upload_to="Beats/images/image/")

    # Represents the free mp3 file of the Beat
    mp3_free = models.FileField(verbose_name="mp3 رایگان", upload_to='Beats/files/mp3/free/')

    # Represents the premium mp3 file of the Beat
    mp3_no_tag_in = models.FileField(verbose_name="pm3 پولی", upload_to='Beats/files/mp3/no_tag/')

    # Represents the wav file of the Beat
    wav = models.FileField(verbose_name="فایل wav", upload_to='Beats/files/wav/')

    # Represents the published_status of the Beat
    published_status = models.CharField(max_length=2, choices=Publish.choices, default=Publish.DRAFT)
    # Represents the status of the Beat
    status = models.CharField(max_length=3, choices=Status.choices, default=Status.CHECKIND)

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

    # Represents the created date of the Beat
    created = models.DateTimeField(auto_now_add=True)

    # Represents the updated date of the Beat
    updated = models.DateTimeField(auto_now=True)

    # Managers for the Beat model
    objects = models.Manager()
    accepted = managers.AcceptedManager()
    rejected = managers.RejectedManager()
    checking = managers.CheckingManager()
    published = managers.PublishManager()
    drafts = managers.DraftManager()

    class Meta:
        verbose_name = "بیت"
        verbose_name_plural = "بیت ها"
        ordering = ['-publish']

    def __str__(self):
        return self.title


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