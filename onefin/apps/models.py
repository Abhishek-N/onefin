from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.


class Collections(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movies = models.JSONField()
    title = models.CharField(max_length=56)
    description = models.CharField(max_length=1000)
    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)


class FavouriteGenres(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    favourites = models.CharField(max_length=56)
    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
