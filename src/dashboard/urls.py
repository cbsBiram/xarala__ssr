from django.urls import path
from course import views as course_views
from dashboard import views
from blog import views as blog_views

app_name = "dashboard"

urlpatterns = [
    path("", views.dashboard_view, name="dashboard"),
    path("staff/", views.StaffView.as_view(), name="staff"),
    path("staff/logs/", views.UserLogList.as_view(), name="logs"),
    path(
        "student/courses/",
        course_views.StudentCourseListView.as_view(),
        name="enrolled-courses",
    ),
    path("instructor/", views.InstructorView.as_view(), name="instructor"),
    path("courses/", views.CourseListView.as_view(), name="courses"),
    path("tutorials/", views.TutorialListView.as_view(), name="tutorials"),
    path("create-course/", views.CourseCreateView.as_view(), name="create-course"),
    path(
        "create-tutorial/", views.TutorialCreateView.as_view(), name="create-tutorial"
    ),
    path(
        "<int:pk>/delete-course/",
        views.CourseDeleteView.as_view(),
        name="delete-course",
    ),
    path(
        "<int:pk>/delete-tutorial/",
        views.TutorialDeleteView.as_view(),
        name="delete-tutorial",
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
