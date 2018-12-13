from django.core.management.base import BaseCommand, CommandError
from django.contrib.contenttypes.models import ContentType
from questions.models import Question, Comment, Like, Tag
from user.models import Profile
from django.contrib.auth.models import User
from faker import Faker
import random


fakegen = Faker()
TAGS = ['Django', 'Golang', 'Python', 'MySql', 'Programming', 'Database', 'Game', 'Swift']


def add_tags():
    for elem in TAGS:
        Tag.objects.get_or_create(title=elem)


def add_users(n):
    for i in range(n):
        fake_profile = fakegen.simple_profile()
        fake_password = fakegen.iban()
        user = User.objects.get_or_create(username=fake_profile['username'], password=fake_password, email=fake_profile['mail'])[0]
        user.save()
        profile = Profile.objects.get_or_create(nickname=fake_profile['username'], avatar='uploads/2018/12/04/' + str(random.choice(list(range(1, 37)))) + '.png', user=user)[0]
        profile.save()


def add_questions(n):
    for i in range(n):
        fake_title = fakegen.sentence(nb_words=4, variable_nb_words=True, ext_word_list=None)
        fake_text = fakegen.text(max_nb_chars=random.choice(list(range(64, 128))), ext_word_list=None)
        fake_author = random.choice(Profile.objects.all())
        fake_tags = random.choices(Tag.objects.all(), k=random.choice(list(range(0, 3))))
        question = Question.objects.get_or_create(author=fake_author, title=fake_title, text=fake_text)[0]
        question.save()
        for tag in fake_tags:
            question.tags.add(tag)


def add_comments(n):
    for i in range(n):
        fake_author = random.choice(Profile.objects.all())
        fake_question = random.choice(Question.objects.all())
        fake_text = fakegen.text(max_nb_chars=random.choice(list(range(16, 128))), ext_word_list=None)
        comment = Comment.objects.get_or_create(author=fake_author, question=fake_question, text=fake_text)[0]
        comment.save()


def add_likes_for_questions(n):
    for i in range(n):
        fake_question = random.choice(Question.objects.all())
        fake_user = random.choice(Profile.objects.all())
        question_type = ContentType.objects.get_for_model(fake_question)
        if not Like.objects.filter(user=fake_user, content_type=question_type, object_id=fake_question.id).exists():
            like = Like.objects.get_or_create(user=fake_user, state=True, content_type=question_type,
                                              object_id=fake_question.id)[0]
            like.save()


def add_likes_for_comments(n):
    for i in range(n):
        fake_comment = random.choice(Comment.objects.all())
        fake_user = random.choice(Profile.objects.all())
        comment_type = ContentType.objects.get_for_model(fake_comment)
        if not Like.objects.filter(user=fake_user, content_type=comment_type, object_id=fake_comment.id).exists():
            like = Like.objects.get_or_create(user=fake_user, state=True, content_type=comment_type,
                                              object_id=fake_comment.id)[0]
            like.save()


class Command(BaseCommand):
    help = 'Add tags, users, question, comments and likes'

    def add_arguments(self, parser):
        parser.add_argument('number_of_users', type=int)

    def handle(self, *args, **options):
        if options['number_of_users']:
            number = options['number_of_users']
            self.stdout.write('-Adding tags', ending='\n')
            add_tags()
            self.stdout.write('-Adding users', ending='\n')
            add_users(number)
            self.stdout.write('-Adding questions', ending='\n')
            add_questions(10 * number)
            self.stdout.write('-Adding comments', ending='\n')
            add_comments(50 * number)
            self.stdout.write('-Adding likes for questions', ending='\n')
            add_likes_for_questions(100 * number)
            self.stdout.write('-Adding likes for comments', ending='\n')
            add_likes_for_comments(500 * number)
            self.stdout.write('-Well done!', ending='\n')

