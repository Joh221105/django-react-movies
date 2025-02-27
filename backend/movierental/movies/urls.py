from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_all_movies, name='get_all_movies'),
    path('<int:movie_id>/', views.get_movie_by_id, name='get_movie_by_id'), 
    path('create/', views.create_movie, name='create_movie'),  
    path('<int:movie_id>/update/', views.update_movie, name='update_movie'),  
    path('<int:movie_id>/delete/', views.delete_movie, name='delete_movie'),  
    path('genre/<str:genre_name>/', views.get_movies_by_genre_name, name='get_movies_by_genre'),  
]