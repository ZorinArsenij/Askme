from django.urls import path
from questions.views import QuestionsByTagView

urlpatterns = [
    # path('<slug:tag_title>', QuestionsByTagView.as_view(), name='questions_by_tag')
    path('<str:tag_title>', QuestionsByTagView.as_view(), name='questions_by_tag')
]