from django.urls import path
from .views import ShopHomePage

app_name = "shop"

urlpatterns = [path("", ShopHomePage.as_view(), name="products")]
