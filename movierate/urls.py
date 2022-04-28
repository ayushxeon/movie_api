from django.urls import path
from . import views

urlpatterns = [
    path('get-movies/', views.listout),
    path('list-movies/', views.show_movie,name='list'),  
    path('rate-movies/', views.rate_movie,name='rate'),
    path('show-avg-ratings/',views.show_ratings,name='average')
]