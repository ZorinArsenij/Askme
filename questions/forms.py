from django import forms
from django.forms import ModelForm
from questions.models import Question, Tag, Comment
from user.models import Profile
from django.utils.translation import ugettext_lazy as _
from django.db import IntegrityError
from django.contrib.auth.models import User


class QuestionCreateForm(ModelForm):

    title = forms.CharField(max_length=64, widget=forms.TextInput(attrs={"class": "form-control"}))
    text = forms.CharField(max_length=128, widget=forms.Textarea(attrs={"class": "form-control", "rows": "7"}))
    tags = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", "data-role": "tagsinput"}))

    def __init__(self, *args, **kwargs):
        self.author = kwargs.pop("author", None)
        super(QuestionCreateForm, self).__init__(*args, **kwargs)

    def clean_tags(self):
        tags = self.cleaned_data["tags"].split(", ")
        if len(tags) > 3:
            raise forms.ValidationError(
                _("Must be no more than three tags."),
                code="count"
            )
        tag_max_len = Tag._meta.get_field("title").max_length
        for tag in tags:
            if len(tag) > tag_max_len:
                raise forms.ValidationError(
                    _("Maximum tag length should not exceed %(value)d symbols."),
                    code="tag_length",
                    params={"value": tag_max_len}
                )
        return tags


    def save(self, commit=True):
        question = Question()
        question.title = self.cleaned_data["title"]
        question.text = self.cleaned_data["text"]
        question.author = self.author
        question.save()
        for tag in self.cleaned_data["tags"]:
            try:
                question.tags.create(title=tag)
            except IntegrityError:
                question.tags.add(Tag.objects.get(title=tag))
        return question

    class Meta:
        model = Question
        fields = ["title", "text", "tags"]


class CommentCreateForm(ModelForm):

    text = forms.CharField(max_length=128, widget=forms.Textarea(attrs={"class": "form-control", "rows": "7", "placeholder": "Enter your answer here..."}))

    def __init__(self, *args, **kwargs):
        self.author = kwargs.pop("author", None)
        self.question = kwargs.pop("question", None )
        super(CommentCreateForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        comment = Comment()
        comment.text = self.cleaned_data["text"]
        comment.author = self.author
        comment.question = self.question
        comment.save()
        return comment

    class Meta:
        model = Comment
        fields = ["text"]