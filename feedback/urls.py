from django.urls import path
from .views import create_feedback_process, home, register, login_view, logout_view, profile_view, user_list

urlpatterns = [
    path('', home, name='home'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile_view, name='profile'),
    path('user-list/', user_list, name='user-list'),
    path('create-feedback-process/',create_feedback_process, name='create-feedback-process'),
]