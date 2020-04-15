from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import path
from . import views


urlpatterns = [
    path('', views.CourseListView.as_view(), name="courses"),
    path('<slug:slug>/overview', views.CourseOverviewView.as_view(),
         name="course-overview"),
    path('<slug:slug>/', login_required(login_url="login")
         (views.CourseDetailView.as_view()), name="course-detail"),
    path('subscribe_user_to_course/<slug:course_slug>/',
         views.subscribe_user_to_course,
         name="subscribe_user_to_course"),
    path('dashboard/student/courses/', views.StudentCourseListView.as_view(),
         name="enrolled-courses"),
    path('dashboard/teacher/',
         user_passes_test(lambda teacher: teacher.user_type == "TC")
         (views.TeacherCourseListView.as_view()),
         name="created-courses"),
    path('dashboard/teacher/<slug:slug>/',
         views.TeacherChapterListCreateView.as_view(), name="add-chapter"),
    path('dashboard/teacher/<slug:slug>/lesson/',
         views.TeacherLessonListCreateView.as_view(), name="add-lesson"),
]
