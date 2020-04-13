from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path,  include


urlpatterns = [
    path('x_yarou/', admin.site.urls),
    path('', include("pages.urls")),
    # path('accounts/', include('allauth.urls')),
    path('courses/', include("course.urls")),
    path('podcasts/', include("podcast.urls")),
    path('users/', include("users.urls")),
    path('summernote/', include('django_summernote.urls')),
]
if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT)
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT)
