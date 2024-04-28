from django.db import models

class Movie(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    duration = models.IntegerField("Duration(min)")