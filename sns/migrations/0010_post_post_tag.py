# Generated by Django 3.2.9 on 2021-11-17 02:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sns', '0009_auto_20211117_1138'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='post_tag',
            field=models.ManyToManyField(blank=True, to='sns.Tag'),
        ),
    ]