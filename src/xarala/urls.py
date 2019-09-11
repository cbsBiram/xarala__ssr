from django.contrib import admin
from django.urls import path,  include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("pages.urls")),
    path('blog/', include("blog.urls")),
    path('courses/', include("course.urls")),
    path('comments/', include("comments.urls")),
    path('users/', include("users.urls")),
]
