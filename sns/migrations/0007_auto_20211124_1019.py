# Generated by Django 3.2.9 on 2021-11-24 01:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sns', '0006_follow'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='post_id',
        ),
        migrations.RemoveField(
            model_name='post',
            name='user_id',
        ),
        migrations.AddField(
            model_name='post',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='sns.account'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Follow',
        ),
    ]
