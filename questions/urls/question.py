from django.urls import path
from questions.views import QuestionPageView
urlpatterns = [
    path('<int:pk>', QuestionPageView.as_view(), name='question_page')
]