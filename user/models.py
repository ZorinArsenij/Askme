from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    nickname = models.CharField(max_length=32, verbose_name=u'Никнэйм', unique=True)
    avatar = models.ImageField(upload_to='uploads/%Y/%m/%d/', verbose_name=u'Аватар')
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.nickname