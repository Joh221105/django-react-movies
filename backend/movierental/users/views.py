import json
from django.http import JsonResponse
from .models import CustomUser
from django.contrib.auth import authenticate, login, logout

# get all users

def user_list(request):
    if request.method == "GET":
        users = list(CustomUser.objects.values('id', 'username', 'email'))  # retrieves id, username, and email from database              n∫
        return JsonResponse(users, safe=False)  # return a JSON response, safe = false to allow list return
    return JsonResponse({"error": "Invalid request"}, status=405)    # return error if not GET

# create a new user

def create_user(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)  # turn the request body into a dictionary

            # validate required fields
            required_fields = ["username", "email", "password"]
            for field in required_fields:
                if field not in data or not data[field]:
                    return JsonResponse({"error": f"{field} is required"}, status=400)

            # create user in database
            user = CustomUser.objects.create_user(
                username=data['username'],
                email=data['email'],
                password=data['password'],
                phone_number=data.get('phone_number', ''),  
                address=data.get('address', '')  
            )

            # success message
            return JsonResponse({"message": "User created successfully"}, status=201)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Invalid request"}, status=405)    # return error if not POST


# get a user by id

# update user information

# delete a user

# login

# sign out