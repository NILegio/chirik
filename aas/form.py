from django.views.generic.base import View
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.admin import UserAdmin
from django import forms
from aas.models import Character, Blog


class MyUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = Character


class MyUserCreationForm(UserCreationForm):
    password1 = forms.CharField(
        label="Пароль",
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
        fields = ['username', 'password1', 'password2', 'first_name', 'last_name']
        help_texts = {'password': "Must be at least 8 characters."}


def clean_username(self):
    username = self.cleaned_data['username']
    try:
        Character.objects.get(username=username)
    except Character.DoesNotExist:
        return username
    raise forms.ValidationError(self.error_messages['duplicate_username'])




class BlogForm(forms.ModelForm):

    parent = forms.IntegerField(
        widget=forms.HiddenInput,
        required=False
    )

    class Meta:
        model = Blog
        fields = ['text']



class CommentForm(forms.Form):

     parent_comment = forms.IntegerField(
         widget=forms.HiddenInput,
         required=False
     )

     comment_area = forms.CharField(
        label='',
        widget=forms.Textarea
     )
