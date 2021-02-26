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
    path("student/", views.StudentView.as_view(), name="student"),
    path("instructor/", views.InstructorView.as_view(), name="instructor"),
    path("courses/", views.CourseListView.as_view(), name="courses"),
    path("course/create/", views.CourseCreateView.as_view(), name="create-course"),
    path(
        "course/<int:pk>/delete/",
        views.CourseDeleteView.as_view(),
        name="delete-course",
    ),
    path(
        "course/edit/<int:pk>",
        views.CourseUpdateView.as_view(),
        name="update-course",
    ),
    path("submit-course/", views.publish_course, name="submit-course"),
    path("tutorials/", views.TutorialListView.as_view(), name="tutorials"),
    path(
        "tutorial/create/", views.TutorialCreateView.as_view(), name="create-tutorial"
    ),
    path(
        "tutorial/<int:pk>/delete/",
        views.TutorialDeleteView.as_view(),
        name="delete-tutorial",
    ),
    path(
        "tutorial/edit/<int:pk>",
        views.TutorialUpdateView.as_view(),
        name="update-tutorial",
    ),
    path("submit-tutorial/", views.publish_tutorial, name="submit-tutorial"),
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
