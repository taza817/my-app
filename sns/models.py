from django.conf import settings
from django.db import models
from django.db.models.fields.related import OneToOneField
from django.utils import timezone
from django.contrib.auth.models import User


# Create your models here.

class Account(models.Model) :
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=20, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=20, blank=True)
    intro = models.TextField(max_length=400, blank=True, null=True)
    account_image = models.ImageField(upload_to="images", blank=True)

    def follow_num(self) :
        return len(Follow.objects.filter(owner=self))

    def follower_num(self) :
        return len(Follow.objects.filter(follow_target=self))

    def __str__(self) :
        return self.user.username


# Follow
class Follow(models.Model) :
    owner = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='do_follow')
    follow_target = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='accept_follow')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["owner", "follow_target"],
                name="follow_unique"
            ),
        ]


# Post
class Tag(models.Model) :
    name = models.CharField(max_length=50)

    def __str__(self) :
        return self.name


class Post(models.Model) :
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    post_image = models.ImageField(upload_to='images', blank=False)
    caption = models.TextField(max_length=400, blank=True)
    post_date = models.DateTimeField(default=timezone.now)
    post_tag = models.ManyToManyField(Tag, blank=True)
    good = models.ManyToManyField(User, related_name='good_post', blank=True)

    def publish(self) :
        self.save()
    
    def __str__(self) :
        return self.user


# Question
class Q_Tag(models.Model) :
    name = models.CharField(max_length=50)
    tag_count = models.IntegerField(default=0)

    def __str__(self) :
        return self.name


class Question(models.Model) :
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    title = models.CharField(max_length=40, blank=False)
    q_image = models.ImageField(upload_to='images', blank=True)
    text = models.TextField(max_length=1000)
    q_date = models.DateTimeField(default=timezone.now)
    q_tag = models.ManyToManyField(Q_Tag, blank=True)
    q_good = models.ManyToManyField(Account, related_name='good_question', blank=True)

    def publish(self) :
        self.save()
    
    def __str__(self) :
        return self.title


class Answer(models.Model) :
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.TextField(max_length=400, blank=False)
    a_image =  models.ImageField(upload_to='images', blank=True)
    a_date = models.DateTimeField(default=timezone.now)
    a_good = models.ManyToManyField(Account, related_name='good_answer', blank=True)

    def publish(self) :
        self.save()

    def __str__(self) :
        return self.text[:20]
