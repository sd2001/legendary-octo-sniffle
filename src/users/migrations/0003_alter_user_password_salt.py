# Generated by Django 4.1.3 on 2022-11-18 20:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_user_password_salt'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='password_salt',
            field=models.CharField(default=b'$2b$12$6sJKVIylYaxeHatFzLoACO', max_length=255),
        ),
    ]
