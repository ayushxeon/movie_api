from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK,
    HTTP_201_CREATED
)
from rest_framework.response import Response
import json
import requests
from .models import Movie,Rating
from .serializer import MovieSerializer

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def listout(request):
    response_API = requests.get('https://api.themoviedb.org/4/list/1?page=1&api_key=67db3e5fac832005f2c928320eae287a')
    result = response_API.json()
    result = result.get("results")
    for movie in result:
        name=movie.get("original_title")
        release_date=movie.get("release_date")
        about=movie.get("overview")
        Movie.objects.update_or_create(movie_name=name,movie_about=about,release_date=release_date)
    return Response("success")

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def show_movie(request):
    data=Movie.objects.all()
    serializer = MovieSerializer(data,many=True)
    print(serializer.data)
    return Response(serializer.data,status=HTTP_200_OK)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def rate_movie(request):
    username = request.user
    print(username)
    rating=request.data.get("rating")
    movie=request.data.get("movie")
    print(rating,"",movie)
    x=Movie.objects.filter(movie_name=movie).first()
    y=Rating.objects.filter(movie=x,user=request.user).first()
    if not x:
        return Response({"error":"movie does not exist"},status=HTTP_404_NOT_FOUND)
    if not y:
        Rating.objects.create(ratings=rating,movie=x,user=request.user)
    else:
        y.ratings=rating
        y.save()


    return Response({"success":"Movie has been rated"},status=HTTP_200_OK)
    
@api_view(["GET"])
def show_ratings(request):
    all=Movie.objects.all()
    avg_rating = []
    for each in all:
        rated=Rating.objects.filter(movie=each)
        count=rated.count()
        sum=0
        for rate in rated:
            sum+=float(rate.ratings)
        if(count==0):
            avg="NA"
        else:
            avg=sum/count
        avg_rating.append({"movie":each.movie_name,"Average Rating":avg})
    
    return Response({"Ratings":avg_rating},status=HTTP_200_OK)

