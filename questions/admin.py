from django.contrib import admin
from questions.models import Question, Like, Comment, Tag

# Register your models here.
admin.site.register(Question)
admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(Tag)
