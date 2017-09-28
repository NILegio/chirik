from aas.models import Character, Blog, Commentary
from .form import MyUserCreationForm, MyUserChangeForm
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin

class MyUserAdmin(UserAdmin):
    form = MyUserChangeForm
    add_form = MyUserCreationForm

admin.site.register((Character, Blog, Commentary))
