# Generated by Django 5.0 on 2023-12-22 07:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_alter_otp_type_alter_user_type'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userprofile',
            options={'verbose_name': 'پروفایل کاربر', 'verbose_name_plural': 'پروفایل کاربران'},
        ),
        migrations.AlterModelOptions(
            name='usersocialmedia',
            options={'verbose_name': 'آدرس های فضای مجازی کاربر', 'verbose_name_plural': 'آدرس های فضای مجازی کاربران'},
        ),
    ]
