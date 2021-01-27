import graphene
from course.models import Course

from course.query_types import CourseType
from .cart import Cart


class CartType(graphene.ObjectType):
    quantity = graphene.Int()
    course = graphene.Field(CourseType)


class Query(graphene.ObjectType):
    cart = graphene.List(CartType)

    def resolve_cart(self, info):
        request = info.context
        cart = Cart(request)
        return cart


class AddCourseToCart(graphene.Mutation):
    class Arguments:
        quantity = graphene.Int()
        courseId = graphene.Int()

    cart = graphene.Field(lambda: CartType)

    def mutate(self, info, quantity, courseId):
        request = info.context
        course = Course.objects.get(pk=courseId)
        cart = Cart(request)
        cart.add(course=course, quantity=quantity, override_quantity=True)
        return AddCourseToCart(cart=cart)


class RemoveCourseFromCart(graphene.Mutation):
    cart = graphene.Field(CartType)

    class Arguments:
        courseId = graphene.Int()

    def mutate(self, info, courseId):
        request = info.context
        course = Course.objects.get(pk=courseId)
        cart = Cart(request)
        cart.remove(course)
        return RemoveCourseFromCart(cart=cart)


class Mutation(graphene.ObjectType):
    add_to_cart_cart = AddCourseToCart.Field()
    remove_from_Cart = RemoveCourseFromCart.Field()
