from django.contrib import admin
from .models import Post, Tag, Account, Follow, Question, Answer, QuestionTag, Child

# admin.site.register(User, UserAdmin)
admin.site.register(Post)
admin.site.register(Tag)
admin.site.register(Account)
admin.site.register(Follow)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(QuestionTag)
admin.site.register(Child)

# Register your models here.
