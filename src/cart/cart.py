from decimal import Decimal
from django.conf import settings
from course.models import Course


class Cart(object):
    def __init__(self, request):
        """
        Initialize the cart.
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def __iter__(self):
        """
        Iterate over the items in the cart and get the courses
        from the database.
        """
        course_ids = self.cart.keys()
        # get the course objects and add them to the cart
        courses = Course.objects.filter(id__in=course_ids)

        cart = self.cart.copy()
        for course in courses:
            cart[str(course.id)]["course"] = course

        for item in cart.values():
            item["price"] = Decimal(item["price"])
            item["total_price"] = item["price"] * item["quantity"]
            yield item

    def __len__(self):
        """
        Count all items in the cart.
        """
        return sum(item["quantity"] for item in self.cart.values())

    def add(self, course, quantity=1, override_quantity=False):
        """
        Add a course to the cart or update its quantity.
        """
        course_id = str(course.id)
        if course_id not in self.cart:
            self.cart[course_id] = {"quantity": 0, "price": str(course.price)}
        if override_quantity:
            self.cart[course_id]["quantity"] = quantity
        else:
            self.cart[course_id]["quantity"] += quantity
        self.save()

    def save(self):
        # mark the session as "modified" to make sure it gets saved
        self.session.modified = True

    def remove(self, course):
        """
        Remove a course from the cart.
        """
        course_id = str(course.id)
        if course_id in self.cart:
            del self.cart[course_id]
            self.save()

    def clear(self):
        # remove cart from session
        del self.session[settings.CART_SESSION_ID]
        self.save()

    def get_total_price(self):
        return sum(
            Decimal(item["price"]) * item["quantity"] for item in self.cart.values()
        )
