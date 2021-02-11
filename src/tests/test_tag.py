import pytest

from blog.models import Tag


@pytest.mark.django_db
def test_contact_create():
    tag = Tag.objects.create(
        name="John",
        description="Doe",
    )
    assert tag.name == "John"
    assert tag.description == "Doe"
