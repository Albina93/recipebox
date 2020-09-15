from django.shortcuts import render, HttpResponseRedirect, reverse
from .models import Recipe, Author
# from django.http import Http404
from .forms import AddRecipeForm, AddAuthorForm, LoginForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


# Create your views here.

def index(request):
    recipes = Recipe.objects.all()
    return render(request, 'index.html', {'recipes': recipes})


def details(request, recipe_id):
    recipe = Recipe.objects.filter(id=recipe_id).first()
    favorites = recipe.favorites.all()
    return render(request, 'details.html', {'recipe': recipe, 'favorites' : favorites})

    # try:
    #     recipe = Recipe.objects.get(id=recipe_id)
    # except Recipe.DoesNotExist:
    #     raise(Http404)
    # return render(request, 'details.html', {'recipe': recipe})


def author(request, author_id):
    author = Author.objects.filter(id=author_id).first()
    recipes = Recipe.objects.filter(author=author_id)
    favorites = Recipe.objects.filter(favorites=author.user)
    return render(request, 'author.html', {'author': author,
                  'recipes': recipes, 'favorites': favorites})

    # try:
    #     author = Author.objects.filter(id=author_id).first()
    #     recipes = Recipe.objects.filter(author=author_id)
    # except Author.DoesNotExist:
    #     raise(Http404)
    # return render(request, 'author.html', {'author': author, 
    #               'recipes': recipes})


@login_required
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
                author=request.user.author
            )
            return HttpResponseRedirect(reverse("homepage"))

    form = AddRecipeForm()
    return render(request, "generic_form.html", {"form": form})


@login_required
def edit_recipe(request, recipe_id):
    current_recipe = Recipe.objects.get(id=recipe_id)
    if request.user.is_staff:
        if request.method == 'POST':
            form = AddRecipeForm(request.POST)
            if form.is_valid():
                new_recipe = form.cleaned_data
                current_recipe.title = new_recipe['title']
                current_recipe.description = new_recipe['description']
                current_recipe.required_time = new_recipe['required_time']
                current_recipe.instructions = new_recipe['instructions']
                current_recipe.save()
            return HttpResponseRedirect(reverse('recipedetails',
                                        args=[current_recipe.id]))
    else:
        if request.user == current_recipe.author.user:
            if request.method == 'POST':
                form = AddRecipeForm(request.POST)
                if form.is_valid():
                    new_recipe = form.cleaned_data
                    current_recipe.title = new_recipe['title']
                    current_recipe.description = new_recipe['description']
                    current_recipe.required_time = new_recipe['required_time']
                    current_recipe.instructions = new_recipe['instructions']
                    current_recipe.save()
                return HttpResponseRedirect(reverse('recipedetails',
                                            args=[current_recipe.id]))
        else:
            return render(request, 'noaccess.html')
    form = AddRecipeForm(initial={'title': current_recipe.title,
                                  'description': current_recipe.description,
                                  'required_time': current_recipe.required_time,
                                  'intructions': current_recipe.instructions})
    return render(request, 'generic_form.html', {'form': form})


@login_required
def add_favorite(request, recipe_id):
    current_user = User.objects.get(id=request.user.id)
    current_recipe = Recipe.objects.get(id=recipe_id)
    current_recipe.favorites.add(current_user)
    return render(request, 'details.html', {'recipe': current_recipe})


@login_required
def remove_favorite(request, recipe_id):
    current_user = User.objects.get(id=request.user.id)
    current_recipe = Recipe.objects.get(id=recipe_id)
    current_recipe.favorites.remove(current_user)
    return render(request, 'details.html', {'recipe': current_recipe})


@login_required
def add_author(request):
    if request.user.is_staff:
        if request.method == "POST":
            form = AddAuthorForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                new_user = User.objects.create_user(username=data.get(
                    "username"), password=data.get("password"))
                Author.objects.create(name=data.get(
                    "username"), user=new_user, bio=data.get("bio"))
                login(request, new_user)
            return HttpResponseRedirect(reverse("homepage"))

    else:
        return render(request, "noaccess.html")

    form = AddAuthorForm()
    return render(request, "generic_form.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request, username=data.get(
                "username"), password=data.get("password"))
            if user:
                login(request, user)
                return HttpResponseRedirect(request.GET.get('next', reverse("homepage")))

    form = LoginForm()
    return render(request, "generic_form.html", {'form': form})


# def signup_view(request):
#     if request.method == "POST":
#         form = SignupForm(request.POST)
#         if form.is_valid():
#             data = form.cleaned_data
#             new_user = User.objects.create_user(
#                 username=data.get("username"),
#                 password=data.get("password")
#             )
#             Author.objects.create(name=data.get("username"), user=new_user)
#             login(request, new_user)
#             return HttpResponseRedirect(reverse("homepage"))

#     form = SignupForm()
#     return render(request, "generic_form.html", {'form': form})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("homepage"))
