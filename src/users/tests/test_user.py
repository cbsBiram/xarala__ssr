import pytest

from users.models import CustomUser as User, Experience, Education, ResetCode


@pytest.mark.django_db
def test_user_create():
    user = User.objects.create(email="test@test.com")
    assert user.email == "test@test.com"


@pytest.mark.django_db
def test_experience_create():
    user = User.objects.create(email="test@test.com")

    experience = Experience.objects.create(
        title="Developer", Company="Google", user=user, description="Anything"
    )
    assert experience.title == "Developer"
    assert experience.user == user
    assert experience.Company == "Google"
    assert experience.description == "Anything"


@pytest.mark.django_db
def test_education_create():
    user = User.objects.create(email="test@test.com")

    education = Education.objects.create(
        title="Master degree", school="Harvard", user=user, description="Anything"
    )
    assert education.title == "Master degree"
    assert education.user == user
    assert education.school == "Harvard"
    assert education.description == "Anything"


@pytest.mark.django_db
def test_reset_code_create():
    reset_code = ResetCode.objects.create(
        code="X2D9",
        email="test@test.com",
    )

    assert reset_code.code == "X2D9"
    assert reset_code.email == "test@test.com"
