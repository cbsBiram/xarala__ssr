from django.urls import path
from course import views as course_views
from users import views as users_views
from .views import DashboardView

urlpatterns = [
    path("", DashboardView.as_view(), name="dashboard"),
    path('dashboard/staff/',
         users_views.AdminView.as_view()),
    path('student/courses/',
         course_views.StudentCourseListView.as_view(),
         name="enrolled-courses"),
    path('teacher/courses/',
         course_views.TeacherCourseListView.as_view(),
         name="created-courses"),
    path('teacher/<slug:slug>/',
         course_views.TeacherChapterListCreateView.as_view(), name="add-chapter"),
    path('teacher/<slug:slug>/lesson/',
         course_views.TeacherLessonListCreateView.as_view(), name="add-lesson"),
]
