from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path,  include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("pages.urls")),
    path('blog/', include("blog.urls")),
    path('courses/', include("course.urls")),
    path('events/', include("events.urls")),
    path('comments/', include("comments.urls")),
    path('users/', include("users.urls")),
    path('summernote/', include('django_summernote.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
