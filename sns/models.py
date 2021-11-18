from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User, AbstractUser


# Create your models here.

class Account(models.Model) :
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=20, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=20, blank=True)
    intro = models.TextField(max_length=400, blank=True)
    account_image = models.ImageField(upload_to="plofile_pics", blank=True)
    following = models.ManyToManyField("self", related_name='following', blank=True)    #フォローしているユーザー

    def __str__(self) :
        return self.user.username

# Follow
class Follow(models.Model) :
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    following = models.ManyToManyField(User, related_name='following', blank=True)

    def __str__(self) :
        return self.user.username


# Post
class Tag(models.Model) :
    name = models.CharField(max_length=20)

    def __str__(self) :
        return self.name
    
    class Meta :
        ordering = ('name',)


class Post(models.Model) :
    post_id = models.CharField(max_length=20, default="000")    #投稿を識別できればなんでもいい
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    post_image = models.ImageField(upload_to='images', blank=True)
    caption = models.TextField(max_length=400)
    post_date = models.DateTimeField(default=timezone.now)
    post_tag = models.ManyToManyField(Tag, blank=True)
    good = models.ManyToManyField(User, related_name='good_post', blank=True)

    def publish(self) :
        self.save()
    
    def __str__(self) :
        return self.post_id
    
    class Meta :
        ordering = ["-post_date"]

