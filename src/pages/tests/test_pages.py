import pytest

# from django.urls import reverse
from pages.models import Carousel, Contact, Subscribe


@pytest.mark.django_db
def test_subscribe_create():
    subscribe = Subscribe.objects.create(
        email_id="test@test.com",
    )
    assert subscribe.email_id == "test@test.com"


@pytest.mark.django_db
def test_carousel_create():
    carousel = Carousel.objects.create(title="A carousel")
    assert carousel.title == "A carousel"


@pytest.mark.django_db
def test_contact_create():
    contact = Contact.objects.create(
        full_name="John Doe", email="johndoe@test.com", phone="+221774444444"
    )

    assert contact.full_name == "John Doe"
    assert contact.email == "johndoe@test.com"
    assert contact.phone == "+221774444444"


# @pytest.mark.django_db
# def test_home_view(client):
#     url = reverse("pages:home")
#     response = client.get(url)
#     assert response.status_code == 200
