# Generated by Django 5.0 on 2023-12-24 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('beats', '0010_beat_is_published'),
    ]

    operations = [
        migrations.AddField(
            model_name='beat',
            name='has_active_licence',
            field=models.BooleanField(default=True),
        ),
    ]