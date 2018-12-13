from django.shortcuts import render
from django.views import View
from user.models import Profile
from questions.models import Question, Tag, Comment, Like
from functions.pagination import paginate
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView
from django.urls import reverse
from questions.forms import QuestionCreateForm, CommentCreateForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.contrib.contenttypes.models import ContentType

# Create your views here.

best_members = [
    "Mr.Freeman",
    "Dr.House",
    "Bender",
    "Queen Victoria",
    "V.Pupkin"
]



class AddQuestionView(LoginRequiredMixin, CreateView):
    login_url = "log_in"
    template_name = "add_question/add_question.html"
    form_class = QuestionCreateForm

    def get_form_kwargs(self):
        kwargs = super(AddQuestionView, self).get_form_kwargs()
        kwargs["author"] = Profile.objects.get(user=self.request.user) if self.request.user.is_authenticated else None
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["popular_tags"] = Tag.objects.all()
        context["best_members"] = best_members
        context["user_info"] = Profile.objects.get(user=self.request.user) \
            if self.request.user.is_authenticated else None
        return context

    def get_success_url(self):
        return reverse('question_page', args=(self.object.id,))


@method_decorator(login_required(login_url="log_in"), name='post')
class QuestionPageView(DetailView, CreateView):
    template_name = "question/question.html"
    form_class = CommentCreateForm
    model = Question

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        if "object_type_404" in context:
            return render(self.request, "page_404.html", context)
        else:
            return self.render_to_response(context)

    def get_form_kwargs(self):
        kwargs = super(QuestionPageView, self).get_form_kwargs()
        kwargs["author"] = Profile.objects.get(user=self.request.user) if self.request.user.is_authenticated else None
        kwargs["question"] = Question.objects.get(pk=self.kwargs["pk"])
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["popular_tags"] = Tag.objects.all()
        context["best_members"] = best_members
        context["user_info"] = Profile.objects.get(
            user=self.request.user) if self.request.user.is_authenticated else None
        try:
            question = Question.objects.get(pk=self.kwargs["pk"])
        except ObjectDoesNotExist:
            context["object_type_404"] = "Question"
            context["message_404"] = "Ooops, there is no question with this id("
            return context

        elements_per_page = 3
        comments = Comment.objects.filter(question__id=self.kwargs["pk"])
        if "comment_id" in self.request.GET:
            page = Comment.objects.filter(question__id=self.kwargs["pk"], pk__gt=self.request.GET.get("comment_id")).count() % elements_per_page
        else:
            page = self.request.GET.get("page")
        comment_list, _ = paginate(comments, page, elements_per_page=elements_per_page)
        context["question"] = question
        context["comments"] = comment_list
        return context

    # def get_new_comment_page(self):


    def get_success_url(self):
        # return reverse("question_page", args=(self.kwargs["pk"], self.object.io)) + "#" + str(self.object.id)
        return "{url}?comment_id={comment_id}#{comment_id}".format(url=reverse("question_page", args=(self.kwargs["pk"],)), comment_id=str(self.object.id))


class NewQuestionsView(View):
    def get(self, request):
        questions_list, _ = paginate(Question.objects.get_new(), request.GET.get("page"))
        context = {
            "new_questions": questions_list,
            "popular_tags": Tag.objects.all(),
            "best_members": best_members,
            "user_info": Profile.objects.get(user=request.user) if request.user.is_authenticated else None
        }
        return render(request, "new_questions/new_questions.html", context)


class QuestionsByTagView(View):
    def get(self, request, tag_title):
        try:
            tag = Tag.objects.get(title=tag_title)
        except ObjectDoesNotExist:
            context = {
                "object_type_404": "Tag",
                "message_404": "Ooops, there is no tag with this title(",
                "popular_tags": Tag.objects.all(),
                "best_members": best_members,
                "user_info": Profile.objects.get(user=request.user) if request.user.is_authenticated else None
            }
            return render(request, "page_404.html", context)
        questions_list, _ = paginate(Question.objects.get_by_tag(tag.title), request.GET.get("page"))
        context = {
            "questions": questions_list,
            "popular_tags": Tag.objects.all(),
            "best_members": best_members,
            "tag_title": tag.title,
            "user_info": Profile.objects.get(user=request.user) if request.user.is_authenticated else None
        }
        return render(request, "questions_by_tag/questions_by_tag.html", context)


class TopQuestionsView(View):
    def get(self, request):
        questions_list, _ = paginate(Question.objects.get_hot(), request.GET.get("page"))
        context = {
            "top_questions": questions_list,
            "popular_tags": Tag.objects.all(),
            "best_members": best_members,
            "user_info": Profile.objects.get(user=request.user) if request.user.is_authenticated else None
        }
        return render(request, "top_questions/top_questions.html", context)


@method_decorator(login_required(login_url="log_in"), name='post')
class LikeView(View):

    def get(self, request, pk):
        if not request.user.is_authenticated:
            return JsonResponse({
                "like": False
            })
        like_type = request.GET.get("type", "")
        like = self.get_like(request, pk, like_type)
        if like:
            return JsonResponse({
                "like": like.state
            })
        else:
            return JsonResponse({
                "like": False
            })

    def post(self, request, pk):
        if not request.user.is_authenticated:
            return JsonResponse({
                "like": False
            })
        like_type = request.POST.get("type", "")
        like = self.get_like(request, pk, like_type)
        if like:
            like.state = not like.state
            like.save()
            return JsonResponse({
                "like": like.state
            })
        else:
            # new_like = Like()
            # new_like.user = Profile.objects.get(user=request.user)
            # if like_type == "Comment":
            #     object = Comment.objects.get(pk=pk)
            #     new_like.content_object = object
            #     new_like.content_type = ContentType.objects.get_for_model(object)
            # elif like_type == "Question":
            #     object = Question.objects.get(pk=pk)
            #     new_like.content_object = object
            #     new_like.content_type = ContentType.objects.get_for_model(object)
            # new_like.object_id = pk
            # new_like.state = True
            # new_like.save()
            profile = Profile.objects.get(user=request.user)
            if like_type == "Comment":
                object = Comment.objects.get(pk=pk)
                like = Like.objects.get_or_create(user=profile, state=True,
                                                  content_type=ContentType.objects.get_for_model(object),
                                                  content_type__model=like_type,
                                                  object_id=pk)[0]
                like.save()
            elif like_type == "Question":
                object = Question.objects.get(pk=pk)
                like = Like.objects.get_or_create(user=profile, state=True,
                                                  content_type=ContentType.objects.get_for_model(object),
                                                  content_type__model=like_type,
                                                  object_id=pk)[0]
                like.save()
            return JsonResponse({
                "like": True
            })

    # def post(self, request, pk):
    #     if request.GET.get("type", "") == "comment":
    #         if
    #         new_like = Like()
    #         new_like.user = request.user
    #         new_like.content_type = comment_type
    #         new_like.object_id = comment_id
    #         new_like.state = True
    #         new_like.save()
    #         update_like = like.first()
    #         update_like.state = True

    def get_like(self, request, pk, like_type):
        profile = Profile.objects.get(user=request.user)
        like = Like.objects.filter(user=profile, content_type__model=like_type, object_id=pk)
        if like.exists():
            return like.first()
        else:
            return None




