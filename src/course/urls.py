from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views


urlpatterns = [
    path('', views.CourseListView.as_view(), name="courses"),
    path('<slug:slug>/overview',
         login_required(views.CourseOverviewView.as_view()), name="course-overview"),
    path('<slug:slug>/',
         views.CourseDetailView.as_view(), name="course-detail"),
    path('subscribe_user_to_course/<slug:course_slug>/', views.subscribe_user_to_course,
         name="subscribe_user_to_course"),
]
