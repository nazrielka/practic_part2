from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('profile/', views.profile, name='profile'),
    path('my_submissions/', views.my_submissions, name='my_submissions'),
    path('submission/create/', views.submission_create, name='create_submission'),
    path('<int:submission_id>/', views.submission_detail, name='detail'),
]