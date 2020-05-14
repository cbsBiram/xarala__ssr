from django.urls import path
from . import views


urlpatterns = [
    path('courses/', views.CourseListView.as_view(), name="courses"),
    path('courses/<slug:slug>/overview', views.CourseOverviewView.as_view(),
         name="course-overview"),
    path('courses/<slug:slug>/',
         views.CourseDetailView.as_view(),
         name="course-detail"),
    path('courses/subscribe-user-to-course/<slug:course_slug>/',
         views.subscribe_user_to_course,
         name="subscribe_user_to_course"),
    path('courses/category/<category>/', views.CategoryCourseList.as_view(),
         name="course-by-category"),
    path("professional-training/",
         views.ProfessionalTrainingView.as_view(), name="professional-training"),
    path("learning-path/",
         views.LearningPathView.as_view(), name="learning-path"),
]
