from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, Post
from mdeditor.fields import MDTextFormField
from django.forms import ModelForm
from django.db import models
from mdeditor.fields import MDTextFormField
class MarkdownForm(forms.Form):
    content = MDTextFormField(label="")