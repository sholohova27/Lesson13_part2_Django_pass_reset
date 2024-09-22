# quotes/models.py (PostgreSQL models)
from django.contrib.auth.models import User
from django.db import models

class Author(models.Model):
    fullname = models.CharField(max_length=255)
    born_date = models.CharField(max_length=255, blank=True, null=True)
    born_location = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.fullname

class Quote(models.Model):
    tags = models.JSONField(default=list)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    quote = models.TextField()

    def __str__(self):
        return self.quote
