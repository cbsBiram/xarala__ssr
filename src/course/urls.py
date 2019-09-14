from django.urls import path
from . import views


urlpatterns = [
    path('', views.CourseListView.as_view(), name="courses"),
    path('<slug:slug>/', views.CourseDetailView.as_view(), name="course-detail"),
    path('lesson/<slug:slug>/',
         views.LessonDetailView.as_view(), name="lesson-detail"),
]
