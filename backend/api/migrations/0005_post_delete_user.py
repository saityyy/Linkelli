# Generated by Django 4.2.3 on 2023-08-08 07:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('socialaccount', '0003_extra_data_default_dict'),
        ('api', '0004_rename_create_date_user_created'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('post_id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('username', models.CharField(max_length=20)),
                ('provider', models.CharField(max_length=20)),
                ('uid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='socialaccount.socialaccount')),
            ],
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]
