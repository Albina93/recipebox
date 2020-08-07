from django.urls import path
from . import views

# recipes/
# recipes/1

urlpatterns = [
    path('', views.index, name="recipe_index"),
    path('recipes/<int:recipe_id>/', views.details, name="recipe_details"),
    path('author/<int:author_id>/', views.author, name="author")

]
