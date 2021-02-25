from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from graphene_django.views import GraphQLView
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path("x-yarou/", admin.site.urls),
    path("graphql/", csrf_exempt(GraphQLView.as_view(graphiql=settings.DEBUG))),
    path("", include("pages.urls", namespace="pages")),
    path("courses/", include("course.urls", namespace="course")),
    path("podcasts/", include("podcast.urls", namespace="podcast")),
    path("users/", include("users.urls")),
    path("tutoriels/", include("blog.urls", namespace="blog")),
    path("path/", include("learning_path.urls", namespace="learning_path")),
    path("dashboard/", include("dashboard.urls", namespace="dashboard")),
    # path("quiz/", include("quiz.urls", namespace="quiz")),
    path("cart/", include("cart.urls", namespace="cart")),
    path("orders/", include("order.urls", namespace="orders")),
    path("payment/", include("payment.urls", namespace="payment")),
    path("search/", include("search.urls", namespace="search")),
    path("summernote/", include("django_summernote.urls")),
    path("oauth/", include("social_django.urls", namespace="social")),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
