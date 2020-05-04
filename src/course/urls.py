from django.urls import path
from . import views


urlpatterns = [
    path('', views.CourseListView.as_view(), name="courses"),
    path('<slug:slug>/overview', views.CourseOverviewView.as_view(),
         name="course-overview"),
    path('<slug:slug>/',
         views.CourseDetailView.as_view(),
         name="course-detail"),
    path('subscribe-user-to-course/<slug:course_slug>/',
         views.subscribe_user_to_course,
         name="subscribe_user_to_course"),
    path('category/<category>/', views.CategoryCourseList.as_view(),
         name="course-by-category"),
    path("course/professional-training/",
         views.ProfessionalTrainingView.as_view(), name="professional-training"),
    path("course/learning-path/",
         views.LearningPathView.as_view(), name="learning-path"),
]
