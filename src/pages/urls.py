from django.urls import path
from . import views

app_name = "pages"

urlpatterns = [
    path("", views.home, name="home"),
    path("subscribe/", views.subscribe, name="subscribe"),
    path("about/", views.about, name="about"),
    path("privacy-policy/", views.privacy_policy, name="privacy_policy"),
    path("community/", views.community_page, name="community"),
    path("team/", views.team_page, name="team"),
    path("faq/", views.faq, name="faq"),
    path("contact/", views.ContactUsView.as_view(), name="contact"),
    path("become-teacher/", views.teacher_registration, name="become-teacher"),
    path("thanks/", views.ThanksView.as_view(), name="thanks"),
]
