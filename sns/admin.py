from django.contrib import admin
from .models import Post, Tag, Account, Follow, Question, Answer, Q_Tag

admin.site.register(Post)
admin.site.register(Tag)
admin.site.register(Account)
admin.site.register(Follow)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Q_Tag)

# Register your models here.
