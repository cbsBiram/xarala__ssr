import graphene
from course.models import Course

from course.query_types import CourseType
from cart.cart import Cart


class CartType(graphene.ObjectType):
    quantity = graphene.Int()


class CreateCart(graphene.Mutation):
    cart = graphene.Field(CartType)

    class Arguments:
        quantity = graphene.Int()
        courseId = graphene.Int()

    def mutate(self, info, quantity, courseId):
        request = info.context
        course = Course.objects.get(pk=courseId)
        cart = Cart(request)
        cart.add(course, quantity)
        return CreateCart(cart=cart)


class Mutation(graphene.ObjectType):
    create_cart = CreateCart.Field()
