from django.urls import path
from . import views

urlpatterns = [
    path('get-movies/', views.get_movies_from_api),
    path('list-movies/', views.list_movie,name='list'),  
    path('rate-movies/', views.rate_movie,name='rate'),
    path('show-avg-ratings/',views.show_avg_ratings,name='average')
]