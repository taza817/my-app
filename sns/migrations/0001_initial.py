# Generated by Django 2.2.24 on 2021-11-06 00:25

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Psot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caption', models.CharField(max_length=400)),
                ('post_date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]