# Generated by Django 4.2.3 on 2023-08-12 10:25

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0024_link_title'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('user_id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20)),
                ('icon_image', models.CharField(max_length=30)),
            ],
        ),
    ]
