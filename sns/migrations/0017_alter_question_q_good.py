# Generated by Django 3.2.9 on 2021-12-01 01:31

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sns', '0016_question_q_good'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='q_good',
            field=models.ManyToManyField(blank=True, related_name='good_question', to=settings.AUTH_USER_MODEL),
        ),
    ]
