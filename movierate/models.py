from tkinter.tix import MAX
from django.db import models
from django.contrib.auth.models import User\

class Movie(models.Model):
    movie_name=models.CharField(max_length=128)
    movie_about=models.CharField(max_length=1500)
    release_date=models.CharField(max_length=128)
    

    def __str__(self):
        return f"{self.movie_name}"


class Rating(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    movie= models.ForeignKey(Movie,on_delete=models.CASCADE,related_name="rating")
    ratings=models.CharField(null=True,blank=True,max_length=12)

    def __str__(self):
        return f"{self.movie}/{self.user}"





