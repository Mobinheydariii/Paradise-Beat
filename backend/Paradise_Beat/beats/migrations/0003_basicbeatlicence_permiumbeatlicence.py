# Generated by Django 5.0 on 2023-12-17 11:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('beats', '0002_beat_published_status_alter_beat_image_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='BasicBeatLicence',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.BigIntegerField(verbose_name='قیمت')),
                ('status', models.CharField(choices=[('AC', 'Active'), ('EX', 'Expired')], default='AC', max_length=2)),
                ('beat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='beat_basic_lisence', to='beats.beat', verbose_name='بیت')),
            ],
        ),
        migrations.CreateModel(
            name='PermiumBeatLicence',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.BigIntegerField(verbose_name='قیمت')),
                ('status', models.CharField(choices=[('AC', 'Active'), ('EX', 'Expired')], default='AC', max_length=2)),
                ('beat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='beat_permium_lisence', to='beats.beat', verbose_name='بیت')),
            ],
        ),
    ]
