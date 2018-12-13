from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import FormView
from django.views.generic.edit import UpdateView, FormView
from django.contrib.auth.mixins import UserPassesTestMixin
from user.models import Profile
from questions.models import Tag
from user.forms import UserLoginForm, UserRegisterForm, UserSettingsForm
from django.contrib.auth import authenticate, login, REDIRECT_FIELD_NAME
from django.contrib.auth.views import LoginView
from django.utils.http import is_safe_url
from django.urls import reverse
from django.shortcuts import get_object_or_404

# Create your views here.

best_members = [
    "Mr.Freeman",
    "Dr.House",
    "Bender",
    "Queen Victoria",
    "V.Pupkin"
]


# class UserSettingsView(View):
#     def get(self, request):
#         context = {
#             "popular_tags": Tag.objects.all(),
#             "best_members": best_members,
#             "user_info": Profile.objects.get(user=request.user) if request.user.is_authenticated else None
#         }
#         return render(request, 'user_settings/user_settings.html', context)


# class UserSettingsView(UserPassesTestMixin, UpdateView):
#
#     model = Profile
#     template_name= "user_settings/user_settings.html"
#     form_class = UserSettingsForm
#     redirect_field_name = None
#     login_url = "log_in"
#
#     def get(self, request, *args, **kwargs):
#         if self.request.user.pk != self.kwargs["pk"]:
#             redirect("user_settings", pk=self.request.user.pk)
#         return super().get(self, request, args, kwargs)
#
#     def get_form(self, form_class=None):
#         form = super(UserSettingsView, self).get_form()
#         form.update_initial()
#         return form
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["user_info"] = Profile.objects.get(user=self.request.user) \
#             if self.request.user.is_authenticated else None
#         context["popular_tags"] = Tag.objects.all()
#         context["best_members"] = best_members
#         return context
#
#     def test_func(self):
#         # if self.request.user.is_authenticated:
#         #     if self.request.user.pk != self.kwargs["pk"]:
#         #         redirect("user_settings", pk=self.request.user.pk)
#         #     return True
#         # else:
#         #     return False
#         return self.request.user.is_authenticated
#         # editing_user = get_object_or_404(Profile, pk=self.kwargs["pk"]).user
#         # return self.request.user.is_authenticated and self.request.user == editing_user
#
#     def get_success_url(self):
#         return str(Profile.objects.get(user=self.request.user).pk)

class UserSettingsView(UserPassesTestMixin, UpdateView):

    model = Profile
    template_name= "user_settings/user_settings.html"
    form_class = UserSettingsForm
    redirect_field_name = None
    login_url = "log_in"

    def get_form(self, form_class=None):
        form = super(UserSettingsView, self).get_form()
        form.update_initial()
        return form

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        return queryset.filter(user=self.request.user).get()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_info"] = Profile.objects.get(user=self.request.user) \
            if self.request.user.is_authenticated else None
        context["popular_tags"] = Tag.objects.all()
        context["best_members"] = best_members
        return context

    def test_func(self):
        return self.request.user.is_authenticated

    def get_success_url(self):
        return reverse('user_settings')


class SignUpView(LoginView):
    template_name = "sign_up/sign_up.html"
    form_class = UserRegisterForm
    redirect_authenticated_user = True

    def __init__(self):
        super().__init__()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["popular_tags"] = Tag.objects.all()
        context["best_members"] = best_members
        return context


class LogInView(LoginView):
    template_name = "log_in/log_in.html"
    form_class = UserLoginForm

    def __init__(self):
        super().__init__()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["popular_tags"] =  Tag.objects.all()
        context["best_members"] = best_members
        return context