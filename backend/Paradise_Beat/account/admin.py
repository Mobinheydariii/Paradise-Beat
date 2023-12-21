from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserChangeForm, UserCreationForm
from . import models



class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ["username", "type", "phone", "email", "is_admin"]
    list_filter = ["is_admin", "type"]
    fieldsets = [
        ("طلاعات کاربر", {"fields": ["username", "phone", "email", "type"]}),
        ("دسترسی های کاربر", {"fields": ["is_admin", "is_active"]})
    ]
    search_fields = ["username", "phone", "email", "type"]
    ordering = ["type", "joined"]

# Now register the new UserAdmin...
admin.site.register(models.User, UserAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)


admin.site.register(models.UserFollower)
admin.site.register(models.UserFollowing)

@admin.register(models.UserProfile)
class AdminUserProfile(admin.ModelAdmin):
    list_display = ["user", "full_name", "bio"]
    ordering = ["user"]
    search_fields = ["user", "full_name"]


admin.site.register(models.UserSocialMedia)