from django.urls import path
from course import views as course_views
from .views import DashboardView, UserLogList, StaffView
from blog import views as blog_views

app_name = "dashboard"

urlpatterns = [
    path("", DashboardView.as_view(), name="dashboard"),
    path("staff/", StaffView.as_view(), name="staff"),
    path("staff/logs/", UserLogList.as_view(), name="logs"),
    path(
        "student/courses/",
        course_views.StudentCourseListView.as_view(),
        name="enrolled-courses",
    ),
    path(
        "teacher/courses/",
        course_views.TeacherCourseListView.as_view(),
        name="created-courses",
    ),
    path(
        "teacher/<slug:slug>/",
        course_views.TeacherChapterListCreateView.as_view(),
        name="add-chapter",
    ),
    path(
        "teacher/<slug:slug>/lesson/",
        course_views.TeacherLessonListCreateView.as_view(),
        name="add-lesson",
    ),
    path(
        "author/posts/",
        blog_views.PostListCreateView.as_view(),
        name="posts-management",
    ),
]
