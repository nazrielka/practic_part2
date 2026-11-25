from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('profile/', views.SubmissionListViewMyProfile.as_view(), name='profile'),

    path('my_submissions/', views.SubmissionListViewMy.as_view(), name='my_submissions'),
    path('submission/create/', views.submission_create, name='create_submission'),
    path('<int:submission_id>/', views.submission_detail, name='detail'),

    path('register/', views.register, name='register'),
]