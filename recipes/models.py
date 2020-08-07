from django.db import models
from django.utils import timezone

# Create your models here.


class Author(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField()

    def __str__(self):
        return self.name


class Recipe(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    required_time = models.CharField(max_length=100)
    instructions = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    date_created = models.DateTimeField(default=timezone.now)
