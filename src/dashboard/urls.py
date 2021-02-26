from django.urls import path
from course import views as course_views
from blog import views as blog_views
from dashboard.views import staff as staff_views
from dashboard.views import student as student_views
from dashboard.views import teacher as teacher_views
from dashboard.views import shared as shared_views

app_name = "dashboard"

urlpatterns = [
    path("", shared_views.dashboard_view, name="dashboard"),
    # staff
    path("staff/", staff_views.StaffView.as_view(), name="staff"),
    path("staff/logs/", staff_views.UserLogList.as_view(), name="logs"),
    path(
        "staff/all-courses/", staff_views.AllCoursesView.as_view(), name="all_courses"
    ),
    path(
        "staff/published-courses/",
        staff_views.PublishedCoursesView.as_view(),
        name="published_courses",
    ),
    path(
        "staff/unpublished-courses/",
        staff_views.UnPublishedCoursesView.as_view(),
        name="unpublished_courses",
    ),
    path(
        "staff/all-tutorials/",
        staff_views.AllTutorialsView.as_view(),
        name="all_tutorials",
    ),
    path(
        "staff/published-tutorials/",
        staff_views.PublishedTutorialsView.as_view(),
        name="published_tutorials",
    ),
    path(
        "staff/unpublished-tutorials/",
        staff_views.UnPublishedTutorialsView.as_view(),
        name="unpublished_tutorials",
    ),
    # student
    path(
        "student/courses/",
        course_views.StudentCourseListView.as_view(),
        name="enrolled-courses",
    ),
    path("student/", student_views.StudentView.as_view(), name="student"),
    # teacher
    path("instructor/", teacher_views.InstructorView.as_view(), name="instructor"),
    path("courses/", teacher_views.CourseListView.as_view(), name="courses"),
    path(
        "course/create/", teacher_views.CourseCreateView.as_view(), name="create-course"
    ),
    path(
        "course/<int:pk>/delete/",
        teacher_views.CourseDeleteView.as_view(),
        name="delete-course",
    ),
    path(
        "course/edit/<int:pk>",
        teacher_views.CourseUpdateView.as_view(),
        name="update-course",
    ),
    path("submit-course/", teacher_views.publish_course, name="submit-course"),
    path("tutorials/", shared_views.TutorialListView.as_view(), name="tutorials"),
    path(
        "tutorial/create/",
        shared_views.TutorialCreateView.as_view(),
        name="create-tutorial",
    ),
    path(
        "tutorial/<int:pk>/delete/",
        shared_views.TutorialDeleteView.as_view(),
        name="delete-tutorial",
    ),
    path(
        "tutorial/edit/<int:pk>",
        shared_views.TutorialUpdateView.as_view(),
        name="update-tutorial",
    ),
    path("submit-tutorial/", shared_views.publish_tutorial, name="submit-tutorial"),
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
