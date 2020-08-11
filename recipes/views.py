from django.shortcuts import render, HttpResponseRedirect, reverse
from .models import Recipe, Author
from django.http import Http404
from .forms import AddRecipeForm, AddAuthorForm


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
    try:
        author = Author.objects.get(id=author_id)
        recipes = Recipe.objects.filter(author=author_id)
    except Author.DoesNotExist:
        raise(Http404)
    return render(request, 'author.html', {'author': author, 'recipes': recipes})


def add_recipe(request):
    if request.method == "POST":
        form = AddRecipeForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Recipe.objects.create(
                title=data.get('title'),
                description=data.get('description'),
                required_time=data.get('required_time'),
                instructions=data.get('instructions'),
                author=data.get('author')
            )
            return HttpResponseRedirect(reverse("homepage"))

    form = AddRecipeForm()
    return render(request, "generic_form.html", {"form": form})


def add_author(request):
    if request.method == "POST":
        form = AddAuthorForm(request.POST)
        form.save()
        return HttpResponseRedirect(reverse("homepage"))

    form = AddAuthorForm()
    return render(request, "generic_form.html", {"form": form})
