import pytest

from course.models import Course
from order.models import Order, OrderItem
from users.models import CustomUser as User


@pytest.mark.django_db
def test_order_create():
    order = Order.objects.create(
        first_name="John Doe",
        last_name="Diop",
        email="johndoe@test.com",
    )
    assert order.first_name == "John Doe"
    assert order.email == "johndoe@test.com"


@pytest.mark.django_db
def test_order_item_create():
    order = Order.objects.create(
        first_name="John Doe",
        email="johndoe@test.com",
        last_name="Diop",
    )

    teacher = User.objects.create(email="test@test.com", is_teacher=True)
    course = Course.objects.create(
        title="Python course",
        description="This is a python course",
        teacher=teacher,
    )

    order_item = OrderItem.objects.create(
        order=order,
        course=course,
        price=1000,
    )
    assert order_item.order == order
    assert order_item.course == course
    assert order_item.price == 1000
