from django.urls import path
from . import views

# recipes/
# recipes/1

urlpatterns = [
    path('', views.index, name="homepage"),
    path('recipes/<int:recipe_id>/', views.details, name="recipe_details"),
    path('author/<int:author_id>/', views.author, name="author"),
    path('addrecipe/', views.add_recipe, name="addrecipe"),
    path('addauthor/', views.add_author, name="addauthor")

]
