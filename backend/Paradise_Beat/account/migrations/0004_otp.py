# Generated by Django 4.0.1 on 2023-12-11 18:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_musician_producer_simpleuser_singer_supporter_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Otp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=11, verbose_name='شماره تلقن')),
                ('email', models.EmailField(max_length=254, verbose_name='ایمیل')),
                ('username', models.CharField(max_length=20, verbose_name='نام کربری')),
                ('password', models.CharField(max_length=16)),
                ('password2', models.CharField(max_length=16)),
                ('token', models.CharField(max_length=200)),
                ('code', models.CharField(max_length=6)),
                ('type', models.CharField(choices=[('SIU', 'Simple_user'), ('SIN', 'Singer'), ('PRD', 'Producer'), ('MUC', 'Musician'), ('SPO', 'Supporter')], default='SIU', max_length=3)),
                ('is_used', models.BooleanField(default=False)),
            ],
        ),
    ]
