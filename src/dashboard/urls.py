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
    path(
        "staff/all-teachers/",
        staff_views.AllTeachersView.as_view(),
        name="all_teachers",
    ),
    path(
        "staff/all-students/",
        staff_views.AllStudentsView.as_view(),
        name="all_students",
    ),
    path("publish-tutorial/", staff_views.publish_tutorial, name="publish-tutorial"),
    path("publish-course/", staff_views.publish_course, name="publish-course"),
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
        "course/edit/<int:pk>",
        teacher_views.CourseUpdateView.as_view(),
        name="update-course",
    ),
    path(
        "manage-course/<slug:slug>",
        teacher_views.CourseManagementView.as_view(),
        name="manage-course",
    ),
    path(
        "add-chapter/<slug:slug>/", teacher_views.create_chapter, name="create-chapter"
    ),
    path(
        "update-chapter/<int:id>/",
        teacher_views.update_chapter,
        name="update-chapter",
    ),
    path(
        "delete-chapter/<int:id>/",
        teacher_views.delete_chapter,
        name="delete-chapter",
    ),
    path(
        "draft-chapter/<int:id>/",
        teacher_views.draft_chapter,
        name="draft-chapter",
    ),
    path(
        "manage-chapter/<slug:slug>",
        teacher_views.ChapterManagementView.as_view(),
        name="manage-chapter",
    ),
    path("add-lesson/<slug:slug>/", teacher_views.create_lesson, name="create-lesson"),
    path(
        "update-lesson/<int:id>/",
        teacher_views.update_lesson,
        name="update-lesson",
    ),
    path(
        "delete-lesson/<int:id>/",
        teacher_views.delete_lesson,
        name="delete-lesson",
    ),
    path(
        "draft-lesson/<int:id>/",
        teacher_views.draft_lesson,
        name="draft-lesson",
    ),
    path("submit-course/", teacher_views.submit_course, name="submit-course"),
    path("draft-course/", teacher_views.draft_course, name="draft-course"),
    # shared
    path("tutorials/", shared_views.TutorialListView.as_view(), name="tutorials"),
    path(
        "tutorial/create/",
        shared_views.TutorialCreateView.as_view(),
        name="create-tutorial",
    ),
    path(
        "tutorial/edit/<int:pk>",
        shared_views.TutorialUpdateView.as_view(),
        name="update-tutorial",
    ),
    path("submit-tutorial/", shared_views.submit_tutorial, name="submit-tutorial"),
    path("draft-tutorial/", shared_views.draft_tutorial, name="draft-tutorial"),
    path(
        "tutorials/<str:slug>/overview/",
        shared_views.tutorial_overview,
        name="tutorial_overview",
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
