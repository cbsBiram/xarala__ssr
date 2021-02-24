from django.urls import path
from .views import SearchResultsView, SearchView

app_name = "search"

urlpatterns = [
    path("explorer/", SearchView.as_view(), name="explorer"),
    path("", SearchResultsView.as_view(), name="results"),
]
