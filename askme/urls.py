"""askme URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from questions.views import NewQuestionsView, AddQuestionView, TopQuestionsView, LikeView
from user.views import SignUpView, LogInView, UserSettingsView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', NewQuestionsView.as_view(), name='new_questions'),
    # path('question/', include('questions.urls')),
    path('question/', include('questions.urls.question')),
    path('ask/', AddQuestionView.as_view(),  name='add_question'),
    path('hot/', TopQuestionsView.as_view(), name='top_questions'),
    path('signup/', SignUpView.as_view(), name='sign_up'),
    path('login/', LogInView.as_view(), name='log_in'),
    path('logout/', LogoutView.as_view(), name='log_out'),
    # path('tag/', include('questions_by_tag.urls')),
    path('tag/', include('questions.urls.questions_by_tag')),
    path('settings/', UserSettingsView.as_view(), name='user_settings'),
    path('like_comment/<int:pk>', LikeView.as_view(), name='like_comment'),
    path('like_question/<int:pk>', LikeView.as_view(), name="like_question" )
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
