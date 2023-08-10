# Generated by Django 4.2.3 on 2023-08-10 08:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('socialaccount', '0003_extra_data_default_dict'),
        ('api', '0015_alter_post_post_sender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='post_sender',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='post_sender', to='socialaccount.socialaccount'),
        ),
    ]
