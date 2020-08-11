from django import forms
from .models import Recipe, Author


class AddRecipeForm(forms.Form):
    title = forms.CharField(max_length=80)
    description = forms.CharField(widget=forms.Textarea)
    required_time = forms.CharField(max_length=80)
    instructions = forms.CharField(widget=forms.Textarea)
    author = forms.ModelChoiceField(queryset=Author.objects.all())


class AddAuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ["name", "bio"]
