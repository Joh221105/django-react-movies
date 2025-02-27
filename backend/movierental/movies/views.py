from django.shortcuts import render
from .models import Movie, Genre
from django.http import JsonResponse
import json
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt


# get all movies
def get_all_movies(request):
    if request.method == "GET":
        movies = list(Movie.objects.values(
            "id", "title", "genre", "description", "release_date", "available_copies"
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
@csrf_exempt
def create_movie(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            required_fields = ["title", "genre", "description", "release_date", "available_copies"]
            for field in required_fields:
                if field not in data or not data[field]:
                    return JsonResponse({"error": f"{field} is required"}, status=400)
            
            # retrieves Genre
            try:
                genre = Genre.objects.get(id=data["genre"])
            except Genre.DoesNotExist:
                return JsonResponse({"error": "Invalid genre ID"}, status=400)

            # converts release date string to date object
            try:
                release_date = datetime.strptime(data["release_date"], "%Y-%m-%d").date()
            except ValueError:
                return JsonResponse({"error": "Invalid date format. Use YYYY-MM-DD"}, status=400)

            # add movie to database
            movie = Movie.objects.create(
                title=data["title"],
                genre=genre,
                description=data["description"],
                release_date=release_date,
                available_copies=data["available_copies"]
            )
            return JsonResponse({"message": "Movie created successfully", "movie_id": movie.id}, status=201)
        
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Invalid request"}, status=405)


# update movie
@csrf_exempt
def update_movie(request, movie_id):
    if request.method == "PUT":
        try:
            data = json.loads(request.body)
            movie = Movie.objects.get(id=movie_id)  # retrieve movie from database
            
            # updates fields only if new values are provided
            movie.title = data.get("title", movie.title)
            movie.genre_id = data.get("genre", movie.genre_id)
            movie.description = data.get("description", movie.description)
            
            if "release_date" in data:
                movie.release_date = datetime.strptime(data["release_date"], "%Y-%m-%d").date()

            movie.available_copies = data.get("available_copies", movie.available_copies)

            movie.save()
            return JsonResponse({"message": "Movie updated successfully"})
        except Movie.DoesNotExist:
            return JsonResponse({"error": "Movie not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    
    return JsonResponse({"error": "Invalid request"}, status=405)  


# delete movie
@csrf_exempt
def delete_movie(request, movie_id):
    if request.method == "DELETE":
        try:
            movie = Movie.objects.get(id=movie_id)
            movie.delete()
            return JsonResponse({"message": "Movie deleted successfully"}, status=200)
        except Movie.DoesNotExist:
            return JsonResponse({"error": "Movie not found"}, status=404)
    return JsonResponse({"error": "Invalid request"}, status=405)  


# filter movie by genre
def get_movies_by_genre_name(request, genre_name):
    if request.method == "GET":
        try:
            genre = Genre.objects.get(name__iexact=genre_name)    # searches for genre object by name, case insensitive
            movies = Movie.objects.filter(genre=genre)    # filters movies by genre, returns list
            movies_data = [
                {
                    "id": movie.id,
                    "title": movie.title,
                    "description": movie.description,
                    "release_date": movie.release_date,
                    "available_copies": movie.available_copies,
                }
                for movie in movies
            ]
            return JsonResponse({"genre": genre.name, "movies": movies_data}, safe=False)
        except Genre.DoesNotExist:
            return JsonResponse({"error": "Genre not found"}, status=404)
    return JsonResponse({"error": "Invalid request"}, status=405)

