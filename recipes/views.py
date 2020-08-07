from django.shortcuts import render
from .models import Recipe, Author
from django.http import Http404


# Create your views here.

def index(request):
    recipes = Recipe.objects.all()
    return render(request, 'index.html', {'recipes': recipes})


def details(request, recipe_id):
    try:
        recipe = Recipe.objects.get(id=recipe_id)

    except Recipe.DoesNotExist:
        raise(Http404)
    return render(request, 'details.html', {'recipe': recipe})


def author(request, author_id):
    author = Author.objects.filter(id=author_id).first()
    recipes = Recipe.objects.filter(author=author_id)
    return render(request, 'author.html', {'author': author, 'recipes': recipes})
