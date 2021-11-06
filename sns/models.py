from django.conf import settings
from django.db import models
from django.utils import timezone

# Create your models here.
class Post(models.Model) :
    post_id = models.CharField(max_length=20, default="000")
    # user_id = models.ForeignKey( ,on_delete=models.CASCADE)
    # post_file = FileField()
    caption = models.CharField(max_length=400)
    # post_tag = 
    # post_good_count = IntegerField()
    post_date = models.DateTimeField(default=timezone.now)

    def publish(self) :
        self.save()
    
    def __str__(self) :
        return self.post_id