from django.db import models
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from user.models import Profile
from django.urls import reverse
# from django.utils.text import slugify

# Create your models here.


class QuestionManager(models.Manager):
    def get_new(self):
        return Question.objects.filter(is_active=True)

    def get_hot(self):
        # return sorted(Question.objects.all(), key=lambda question: question.likes.get_number_of_likes(), reverse=True)
        return Question.objects.annotate(num_likes=models.Count('likes__state')).order_by('-num_likes')

    def get_by_tag(self, tag_title):
        return Question.objects.filter(tags__title__contains=tag_title, is_active=True)


class LikeManager(models.Manager):
    def get_number_of_likes(self):
        return self.filter(state=True).count()


class Tag(models.Model):
    title = models.CharField(max_length=16, verbose_name=u'Заголовок тэга', unique=True)
    # slug = models.SlugField(unique=True)

    def get_url(self):
        return reverse('questions_by_tag', kwargs={'tag_title': self.title})

    # def save(self, *args, **kwargs):
    #     self.slug = slugify(self.title)
    #     super(Tag, self).save(*args, **kwargs)


    def __str__(self):
        return self.title


class Like(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    state = models.BooleanField(default=False)
    limit_choices_to = models.Q(app_label='question', model='Question') | models.Q(app_label='question', model='Comment')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, limit_choices_to=limit_choices_to)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    objects = LikeManager()

    class Meta:
        unique_together = ('user', 'content_type', 'object_id')


class Question(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length=64, verbose_name=u'Заголовок вопроса', unique=True)
    text = models.CharField(max_length=128, verbose_name=u'Содержание вопроса')
    create_date = models.DateTimeField(default=timezone.now, verbose_name=u"Время создания вопроса")
    is_active = models.BooleanField(default=True, verbose_name=u"Доступность вопроса")
    tags = models.ManyToManyField(Tag)
    likes = GenericRelation(Like, related_query_name='Question')
    objects = QuestionManager()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-create_date']


class Comment(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=128, verbose_name=u'Содержание комментария')
    correct = models.BooleanField(default=False)
    likes = GenericRelation(Like, related_query_name='Comment', related_name='comment')