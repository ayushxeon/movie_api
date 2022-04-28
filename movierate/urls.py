from django.urls import path
from . import views

urlpatterns = [
    path('get-movies/', views.listout),
    path('list-movies/', views.show_movie),  
    path('rate-movies/', views.rate_movie),
    path('show-avg-ratings/',views.show_ratings)
]