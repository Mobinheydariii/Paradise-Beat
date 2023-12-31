# Generated by Django 5.0 on 2023-12-26 09:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('beats', '0011_beat_has_active_licence'),
    ]

    operations = [
        migrations.CreateModel(
            name='LicenceType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='permiumbeatlicence',
            name='beat',
        ),
        migrations.RemoveField(
            model_name='permiumbeatlicence',
            name='user',
        ),
        migrations.CreateModel(
            name='BeatLicence',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.BigIntegerField()),
                ('beat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='beats.beat')),
                ('licence_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='beats.licencetype')),
            ],
        ),
        migrations.DeleteModel(
            name='BasicBeatLicence',
        ),
        migrations.DeleteModel(
            name='PermiumBeatLicence',
        ),
    ]
