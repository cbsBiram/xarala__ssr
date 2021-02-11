import pytest

from userlogs.models import UserLog
from users.models import CustomUser as User


@pytest.mark.django_db
def test_user_log_create():
    user = User.objects.create(email="test@test.com")
    user_log = UserLog.objects.create(
        user=user, action="Failed to connect!", user_type="student"
    )
    assert user_log.user == user
    assert user_log.action == "Failed to connect!"
    assert user_log.user_type == "student"
