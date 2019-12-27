from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path,  include
from graphene_django.views import GraphQLView
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    # path('jet/', include('jet.urls', 'jet')),
    # path('jet/dasboard/', include('jet.dashboard.urls', 'jet-dashboard')),
    path('x_yarou/', admin.site.urls),
    path('graphql/', csrf_exempt(GraphQLView.as_view(graphiql=True))),
    path('', include("pages.urls")),
    path('blog/', include("blog.urls")),
    path('courses/', include("course.urls")),
    path('events/', include("events.urls")),
    path('comments/', include("comments.urls")),
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
