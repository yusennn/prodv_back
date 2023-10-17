from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create_problem, name='create-problem'),
    path('list/', views.problem_list, name='problem-list'),
    path('problem/<int:problem_id>/', views.problem_detail, name='problem-detail'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
]
