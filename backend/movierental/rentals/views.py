from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Rental
from movies.models import Movie
from users.models import CustomUser

# create rental
@csrf_exempt
def create_rental(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user = CustomUser.objects.get(id=data["user_id"])
            movie = Movie.objects.get(id=data["movie_id"])

            rental = Rental.objects.create(user=user, movie=movie)
            return JsonResponse({"message": "Rental created", "rental_id": rental.id}, status=201)
        except CustomUser.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)
        except Movie.DoesNotExist:
            return JsonResponse({"error": "Movie not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)


# get all rentals
def get_all_rentals(request):
    if request.method == "GET":
        rentals = list(Rental.objects.values("id", "user__username", "movie__title", "rented_at", "returned_at"))
        return JsonResponse({"rentals": rentals}, safe=False)

    return JsonResponse({"error": "Invalid request method"}, status=405)


# get rental by id
def get_rental_by_id(request, rental_id):
    if request.method == "GET":
        try:
            rental = Rental.objects.values("id", "user__username", "movie__title", "rented_at", "returned_at").get(id=rental_id)
            return JsonResponse(rental, safe=False)
        except Rental.DoesNotExist:
            return JsonResponse({"error": "Rental not found"}, status=404)

    return JsonResponse({"error": "Invalid request method"}, status=405)


# update/return rental by id
@csrf_exempt
def update_rental(request, rental_id):
    if request.method == "PUT":
        try:
            data = json.loads(request.body)
            rental = Rental.objects.get(id=rental_id)
            if "returned_at" in data:
                rental.returned_at = data["returned_at"]
            rental.save()
            return JsonResponse({"message": "Rental updated"})
        except Rental.DoesNotExist:
            return JsonResponse({"error": "Rental not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)


# delete rental by id
@csrf_exempt
def delete_rental(request, rental_id):
    if request.method == "DELETE":
        try:
            rental = Rental.objects.get(id=rental_id)
            rental.delete()
            return JsonResponse({"message": "Rental deleted"})
        except Rental.DoesNotExist:
            return JsonResponse({"error": "Rental not found"}, status=404)

    return JsonResponse({"error": "Invalid request method"}, status=405)


# gets all non-returned/active rentals
def get_active_rentals(request):
    active_rentals = Rental.objects.filter(returned_at__isnull=True).values(
        "id", "user__username", "movie__title", "rented_at"
    )
    return JsonResponse(list(active_rentals), safe=False)


# gets all rentals for a specific user
def get_rentals_by_user(request, username):
    rentals = Rental.objects.filter(user__username=username).values(
        "id", "movie__title", "rented_at", "returned_at"
    )
    return JsonResponse(list(rentals), safe=False)