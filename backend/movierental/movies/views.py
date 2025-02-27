from django.shortcuts import render
from .models import Movie
from django.http import JsonResponse
import json

# get all movies

def get_all_movies(request):
    if request.method == "GET":
        movies = list(Movie.objects.values(
            "id", "title", "genre_name", "description", "release_date", "available_copies"
        ))
        return JsonResponse(movies, safe=False)
    return JsonResponse({"error": "Invalid request"}, status=405)



# get movie by id

def get_movie_by_id(request, movie_id):
    if request.method == "GET":
        try:
            movie = Movie.objects.get(id=movie_id)
            return JsonResponse({
                "id": movie.id,
                "title": movie.title,
                "genre": movie.genre.name if movie.genre else None,
                "description": movie.description,
                "release_date": movie.release_date,
                "available_copies": movie.available_copies
            })
        except Movie.DoesNotExist:
            return JsonResponse({"error": "Movie not found"}, status=404)
    return JsonResponse({"error": "Invalid request"}, status=405)

# create movie

# update movie

# delete movie

# filter movie by genre