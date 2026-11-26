from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('profile/', views.SubmissionListViewMyProfile.as_view(), name='profile'),

    path('my_submissions/', views.SubmissionListViewMy.as_view(), name='my_submissions'),
    path('submissions/<int:pk>/', views.SubmissionDetailView.as_view(), name='submission-detail'),
    path('submission/create/', views.SubmissionCreateView.as_view(), name='create_submission'),
    path('submission/<int:pk>/update/', views.SubmissionUpdateView.as_view(), name='update_submission'),
    path('submission/<int:pk>/delete/', views.SubmissionDeleteView.as_view(), name='delete_submission'),

    path('all_submissions/', views.SubmissionListViewAll.as_view(), name='all_submissions'),
    path('design/<int:pk>/create/', views.DesignCreateView.as_view(), name='create_design'),

    path('categories/', views.CategoryListView.as_view(), name='categories'),
    path('categories/create', views.CategoryCreateView.as_view(), name='create_category'),
    path('category/<int:pk>/delete', views.CategoryDeleteView.as_view(), name='delete_category'),

    path('register/', views.register, name='register'),
]