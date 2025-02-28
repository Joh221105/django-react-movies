from django.urls import path
from . import views

urlpatterns = [
    path("create/", views.create_rental, name="create-rental"),  
    path("all/", views.get_all_rentals, name="all-rentals"),  
    path("<int:rental_id>/", views.get_rental_by_id, name="rental-by-id"), 
    path("update/<int:rental_id>/", views.update_rental, name="update-rental"), 
    path("delete/<int:rental_id>/", views.delete_rental, name="delete-rental"), 
    path("active/", views.get_active_rentals, name="active-rentals"), 
    path("user/<str:username>/", views.get_rentals_by_user, name="rentals-by-user"),  
]
