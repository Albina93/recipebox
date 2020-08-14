from django import forms
from .models import Recipe, Author


class AddRecipeForm(forms.Form):
    title = forms.CharField(max_length=80)
    description = forms.CharField(widget=forms.Textarea)
    required_time = forms.CharField(max_length=80)
    instructions = forms.CharField(widget=forms.Textarea)
    # author = forms.ModelChoiceField(queryset=Author.objects.all())


class AddAuthorForm(forms.Form):
    username = forms.CharField(max_length=240)
    bio = forms.CharField(widget=forms.Textarea)
    password = forms.CharField(widget=forms.PasswordInput)


class LoginForm(forms.Form):
    username = forms.CharField(max_length=240)
    password = forms.CharField(widget=forms.PasswordInput)
