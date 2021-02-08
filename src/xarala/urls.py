from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView

urlpatterns = [
    path("x-yarou/", admin.site.urls),
    path("graphql/", csrf_exempt(GraphQLView.as_view(settings.DEBUG))),
    path("", include("pages.urls", namespace="pages")),
    path("", include("course.urls", namespace="course")),
    path("podcasts/", include("podcast.urls", namespace="podcast")),
    path("users/", include("users.urls")),
    path("blog/", include("blog.urls", namespace="blog")),
    path("dashboard/", include("dashboard.urls", namespace="dashboard")),
    path("search/", include("search.urls", namespace="search")),
    path("summernote/", include("django_summernote.urls")),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
