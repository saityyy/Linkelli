# Generated by Django 4.2.3 on 2023-08-28 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_userinfo_user_info_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='anonymous_mode',
            field=models.BooleanField(default=False),
        ),
    ]
