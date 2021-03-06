# Generated by Django 3.2.9 on 2021-11-16 05:29

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sns', '0006_follow'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-post_date']},
        ),
        migrations.AddField(
            model_name='post',
            name='good',
            field=models.ManyToManyField(blank=True, related_name='good_post', to=settings.AUTH_USER_MODEL),
        ),
    ]
