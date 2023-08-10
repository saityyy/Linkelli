# Generated by Django 4.2.3 on 2023-08-10 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0016_alter_post_post_sender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='keyword',
            name='keyword_id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='link',
            name='link_id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='post',
            name='post_id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterUniqueTogether(
            name='link',
            unique_together={('link', 'post_id')},
        ),
    ]
