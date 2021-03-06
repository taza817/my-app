# Generated by Django 3.2.9 on 2021-12-13 01:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sns', '0023_auto_20211211_1236'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Q_Tag',
            new_name='QuestionTag',
        ),
        migrations.RenameField(
            model_name='answer',
            old_name='a_date',
            new_name='answer_date',
        ),
        migrations.RenameField(
            model_name='answer',
            old_name='a_good',
            new_name='answer_good',
        ),
        migrations.RenameField(
            model_name='answer',
            old_name='a_image',
            new_name='answer_image',
        ),
        migrations.RenameField(
            model_name='question',
            old_name='q_date',
            new_name='question_date',
        ),
        migrations.RenameField(
            model_name='question',
            old_name='q_good',
            new_name='question_good',
        ),
        migrations.RemoveField(
            model_name='question',
            name='q_image',
        ),
        migrations.RemoveField(
            model_name='question',
            name='q_tag',
        ),
        migrations.AddField(
            model_name='question',
            name='question_image',
            field=models.ImageField(blank=True, upload_to='images'),
        ),
        migrations.AddField(
            model_name='question',
            name='question_tag',
            field=models.ManyToManyField(blank=True, to='sns.QuestionTag'),
        ),
    ]
