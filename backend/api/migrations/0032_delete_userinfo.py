# Generated by Django 4.2.3 on 2023-08-13 08:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0031_rename_user_id_userinfo_user'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UserInfo',
        ),
    ]
