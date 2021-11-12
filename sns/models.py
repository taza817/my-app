from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# # Foolow中間モデル
# class Frendship(models.Model) :
#     follower = models.ForeignKey('Account', on_delete=models.CASCADE, related_name='followee_friendship')
#     followee = models.ForeignKey('Account', on_delete=models.CASCADE, related_name='follower_friendship')

#     class Meta :
#         unique_together = ('follower', 'followee')


#ExpandUser
class Account(models.Model) :
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=20, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=20, blank=True)
    intro = models.TextField(max_length=400, blank=True)
    account_image = models.ImageField(upload_to="plofile_pics", blank=True)
    # # Follow
    # followees = models.ManyToManyField(
    #     'Account', verbose_name='フォロー中のユーザー', through='Frendship', 
    #     related_name='+', through_fields('follower', 'followee')
    # )
    # followers = models.ManyToManyField(
    #     'Account', verbose_name='フォローされているユーザー', through='Frendship', 
    #     related_name='+', through_fields('followee', 'follower')
    # )

account = Account.objects.get(id=1)
account_email = account.user.email
USERNAME_FIELD = 'some_email'
REQUIRED_FIELDS = ['username']

# Userインスタンスの作成/更新とAccountモデルを同期する
@receiver(post_save, sender=User)
def create_user_account(sender, instance, created, **kwargs) :
    if created :
        Account.objects.create(user=instance)

@receiver(post_save, sender=User) 
def save_user_account(sender, instance, **kwargs) :
    instance.account.save()





#Post

# def random_url() :
#     chars = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
#     url = ''.join(random.choice(chars)for i in range(16))     #.joinで文字列をURLに結合
#     return url

# class Post(models.Model) :
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     # post_file = FileField()
#     caption = models.TextField(max_length=400)
#     post_url = models.UrlField(_('URL'), blank=True)
#     slug = models.SlugField(unique=True, default=random_url)
#     post_date = models.DateTimeField(default=timezone.now)

#     def get_absolute_url(self) :
#         return reversed('series', kwargs={'slug': self.slug})    #urlの指定

#     def publish(self) :
#         self.save()
    
#     def __str__(self) :
#         return self.post_url
