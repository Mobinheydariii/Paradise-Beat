# Generated by Django 5.0 on 2023-12-17 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_alter_otp_type_alter_user_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otp',
            name='type',
            field=models.CharField(choices=[('SIM', 'Simple_user'), ('SIN', 'Singer'), ('PRD', 'Producer'), ('MUC', 'Musician')], default='SIM', max_length=3),
        ),
        migrations.AlterField(
            model_name='user',
            name='type',
            field=models.CharField(choices=[('SIM', 'Simple_user'), ('SIN', 'Singer'), ('PRD', 'Producer'), ('MUC', 'Musician')], max_length=3),
        ),
    ]
