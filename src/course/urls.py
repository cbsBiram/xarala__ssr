from django.urls import path
from . import views


urlpatterns = [
    path('', views.CourseListView.as_view(), name="courses"),
    path('<slug:slug>/overview',
         views.CourseOverviewView.as_view(), name="course-overview"),
    path('<slug:slug>/lecture',
         views.CourseDetailView.as_view(), name="course-detail"),
]
