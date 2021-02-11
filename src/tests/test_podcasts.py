import pytest

from podcast.models import Episode, Guest
from users.models import CustomUser as User


@pytest.mark.django_db
def test_guest_create():
    guest = Guest.objects.create(name="Elias", profession="Developer")
    assert guest.name == "Elias"
    assert guest.profession == "Developer"


@pytest.mark.django_db
def test_episode_create():
    publisher = User.objects.create(email="publisher@test.com")
    guest = Guest.objects.create(name="Elias", profession="Developer")

    episode = Episode.objects.create(
        title="Talk about python",
        description="A short description",
        guest=guest,
        publisher=publisher,
    )
    assert episode.title == "Talk about python"
    assert episode.description == "A short description"
    assert episode.guest == guest
    assert episode.publisher == publisher