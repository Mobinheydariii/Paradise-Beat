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
    list_filter = ["is_admin"]
    fieldsets = [
        ("اطلاعات شخصی", {"fields": ["phone"]}),
        ("طلاعات کاربر", {"fields": ["username", "email", "type"]}),
        ("مجوزهای کاربر", {"fields": ["is_admin", "is_active"]}),
    ]
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["email", "password1", "password2"],
            },
        ),
    ]
    search_fields = ["username", "phone", "email", "type"]
    ordering = ["type", "joined"]
    filter_horizontal = []

# Now register the new UserAdmin...
admin.site.register(models.User, UserAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)


admin.site.register(models.UserFollower)
admin.site.register(models.UserFollowing)
admin.site.register(models.UserProfile)
