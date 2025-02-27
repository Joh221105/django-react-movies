import json
from django.http import JsonResponse
from .models import CustomUser
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt

# get all users

def user_list(request):
    if request.method == "GET":
        users = list(CustomUser.objects.values('id', 'username', 'email'))  # retrieves id, username, and email from database              n∫
        return JsonResponse(users, safe=False)  # return a JSON response, safe = false to allow list return
    return JsonResponse({"error": "Invalid request"}, status=405)    # return error if not GET

# create a new user
@csrf_exempt
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

def get_user(request, user_id):
    try:
        user = CustomUser.objects.get(id=user_id)
        return JsonResponse({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "phone_number": user.phone_number,
            "address": user.address
        })
    except CustomUser.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)


# update user information
@csrf_exempt
def update_user(request, user_id):
    if request.method == "PUT":
        try:
            data = json.loads(request.body)
            user = CustomUser.objects.get(id=user_id)   # retrieves user from database
            user.username = data.get("username", user.username)    # updates username 
            user.email = data.get("email", user.email)    # updates password
            user.phone_number = data.get("phone_number", user.phone_number)    # updates phone number
            user.address = data.get("address", user.address)    # updates address
            if "password" in data:
                user.set_password(data["password"])
            user.save()
            return JsonResponse({"message": "User successfully updated"})
        except CustomUser.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request"}, status=405)   # return error if not PUT

# delete a user

def delete_user(request, user_id):
    if request.method == "DELETE":
        try:
            user = CustomUser.objects.get(id=user_id)
            user.delete()
            return JsonResponse({"message": "User successfully deleted"})
        except CustomUser.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)
    return JsonResponse({"error": "Invalid request"}, status=405)    # return error if not DELETE

# login
@csrf_exempt
def user_login(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user = authenticate(username=data["username"], password=data["password"])   # checks if the username and password exist in db
            if user is not None:
                login(request, user)    # creates a session for the user
                return JsonResponse({"message": "Login successful"})
            return JsonResponse({"error": "Invalid credentials"}, status=401)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request"}, status=405)


# sign out
@csrf_exempt
def user_logout(request):
    if request.method == "POST":
        logout(request)    # removes session data for the user
        return JsonResponse({"message": "Logout successful"})
    return JsonResponse({"error": "Invalid request"}, status=405)