from django.views.generic.base import View
from django.views.generic.edit import FormView
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import login
from django import forms
from aas.models import Character


class MyUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = Character


class MyUserCreationForm(UserCreationForm):
    password1 = forms.CharField(
        label="Password",
        max_length=32,
        required=True,
        widget=forms.PasswordInput
    )

    password2 = forms.CharField(
        label="Confirm",
        max_length=32,
        required=True,
        widget=forms.PasswordInput,
        help_text='Make sure they match'
    )


    class Meta():
        model = Character
        fields = ['username', 'password1', 'password2', 'email', 'first_name', 'last_name']
        help_texts = {'password': "Must be at least 8 characters."}


def clean_username(self):
    username = self.cleaned_data['username']
    try:
        Character.objects.get(username=username)
    except Character.DoesNotExist:
        return username
    raise forms.ValidationError(self.error_messages['duplicate_username'])


class RegView(FormView):
    template_name = 'registration.html'
    form_class = MyUserCreationForm
    success_url = '/login/'

    def form_valid(self, form):
        form.save()
        return super(RegView, self).form_valid(form)


class LoginView(FormView):
    form_class = AuthenticationForm
    template_name = 'login.html'
    success_url = '/'

    def form_valid(self, form):
        self.user = form.get_user()
        login(self.request, self.user)
        return super(LoginView, self).form_valid(form)
