from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_user, name='create_user'),  
    path('<int:user_id>/', views.get_user, name='get_user'), 
    path('<int:user_id>/update/', views.update_user, name='update_user'), 
    path('login/', views.user_login, name='user_login'),  
    path('logout/', views.user_logout, name='user_logout'), 
    path('', views.user_list, name='user_list'),  
]
