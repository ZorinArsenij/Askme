from django import forms
from django.contrib.auth.models import User
from user.models import Profile
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext_lazy as _
from django.forms import ModelForm



class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    error_messages = {
        'invalid_login': "Invalid username or password."
    }


class UserRegisterForm(UserCreationForm):

    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    nickname = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password2 = forms.CharField(
        label="Repeat password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        strip=False
    )
    avatar = forms.ImageField(widget=forms.FileInput(attrs={'class': 'custom-file-input', 'type': 'file'}), required=False)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(UserRegisterForm, self).__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError(
            _('Email %(value)s is already taken.'),
            code='email_unique',
            params={'value': email}
        )

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(
            _('Username %(value)s is already taken.'),
            code='username_unique',
            params={'value': username})

    def clean_nickname(self):
        nickname = self.cleaned_data['nickname']
        try:
            profile = Profile.objects.get(nickname=nickname)
        except Profile.DoesNotExist:
            return nickname
        raise forms.ValidationError(
            _('Nickname %(value)s is already taken.'),
            code='nickname_unique',
            params={'value': nickname})

    def clean_avatar(self):
        avatar = self.cleaned_data['avatar']
        if not avatar:
            return 'user_image/default_user_image.png'
        else:
            return avatar

    def save(self):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email']
        )
        user.set_password(self.cleaned_data['password1'])
        user.save()

        user_profile = Profile.objects.create(
            nickname=self.cleaned_data['nickname'],
            avatar=self.cleaned_data['avatar'],
            user=user
        )
        user_profile.save()
        return user_profile

    def get_user(self):
        return self.save().user


class UserSettingsForm(ModelForm):

    class Meta:
        model = Profile
        fields = ['username', 'email', 'nickname', 'avatar']

    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    nickname = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    avatar = forms.ImageField(widget=forms.FileInput(attrs={'class': 'custom-file-input', 'type': 'file'}), required=False)

    def update_initial(self):
        self.fields['email'].initial = self.instance.user.email
        self.fields['username'].initial = self.instance.user.username
        # self.fields['nickname'] = self.instance.nickname
        # self.fields['avatar'] = self.instance.avatar

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            user = User.objects.get(email=email)
            if user == self.instance.user:
                return email
        except User.DoesNotExist:
            return email
        raise forms.ValidationError(
            _('Email %(value)s is already taken.'),
            code='email_unique',
            params={'value': email}
        )

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            user = User.objects.get(username=username)
            if user == self.instance.user:
                return username
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(
            _('Username %(value)s is already taken.'),
            code='username_unique',
            params={'value': username})

    def clean_nickname(self):
        nickname = self.cleaned_data['nickname']
        try:
            profile = Profile.objects.get(nickname=nickname)
            if profile == self.instance:
                return nickname
        except Profile.DoesNotExist:
            return nickname
        raise forms.ValidationError(
            _('Nickname %(value)s is already taken.'),
            code='nickname_unique',
            params={'value': nickname})


    def save(self, commit=True):
        self.instance.user.email = self.cleaned_data['email']
        self.instance.user.username = self.cleaned_data['username']
        self.instance.user.save()
        self.instance.nickname = self.cleaned_data['nickname']
        if self.cleaned_data['avatar']:
            self.instance.avatar = self.cleaned_data['avatar']
        self.instance.save()
        return self.instance
