from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


#ExpandUser
class Account(models.Model) :
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=20, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=20, blank=True)
    intro = models.TextField(max_length=400, blank=True)
    account_image = models.ImageField(upload_to="plofile_pics", blank=True)
    # USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['username']


@receiver(post_save, sender=User)
def create_user(sender, instance, created, **kwargs) :
    if created :
        Account.objects.create(user=instance)

@receiver(post_save, sender=User) 
def save_user_account(sender, instance, **kwargs) :
    instance.account.save()


#Post
class Post(models.Model) :
    post_id = models.CharField(max_length=20, default="000")
    # user_id = models.ForeignKey(Account, on_delete=models.CASCADE)
    # post_file = FileField()
    caption = models.TextField(max_length=400)
    post_date = models.DateTimeField(default=timezone.now)

    def publish(self) :
        self.save()
    
    def __str__(self) :
        return self.post_id
