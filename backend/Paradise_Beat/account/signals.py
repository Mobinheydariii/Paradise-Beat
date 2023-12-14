from django.db.models.signals import post_save
from .models import User
from . import models



def create_user_profile(sender, instance, created, **kwargs):
    if created:
        models.UserProfile.objects.create(user=instance)

def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)

def create_user_following(sender, instance, created, *args, **kwargs):
    if created:
        models.UserFollowing.objects.create(user=instance)

def save_user_following(sender, instance, **kwargs):
    instance.UserFollowing.save()

post_save.connect(create_user_following, sender=User)
post_save.connect(save_user_following, sender=User)


def create_user_follower(sender, instance, created, *args, **kwargs):
    if created:
        models.UserFollower.objects.create(user=instance)

def save_user_follower(sender, instance, **kwargs):
    instance.UserFollower.save()

post_save.connect(create_user_follower, sender=User)
post_save.connect(save_user_follower, sender=User)


def create_user_social_media(sender, instance, created, *args, **kwargs):
    if created:
        models.UserSocialMedia.objects.create(user=instance)

def save_user_social_media(sender, instance, **kwargs):
    instance.UserSocialMedia.save()

post_save.connect(create_user_social_media, sender=User)
post_save.connect(save_user_social_media, sender=User)