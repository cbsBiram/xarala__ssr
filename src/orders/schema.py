import graphene
from graphql import GraphQLError

from course.models import Course
from .models import Order, OrderItem
from .query_types import OrderType, OrderItemType


class Query(graphene.ObjectType):
    orders = graphene.List(OrderType)
    order = graphene.Field(OrderType, orderId=graphene.Int())

    def resolve_orders(self, info):
        return Order.objects.all()

    def resolve_order(self, info, orderId=None):
        user = info.context.user
        if not orderId:
            order = Order.objects.filter(email=user.email).last()
            return order
        order = Order.objects.get(pk=orderId)
        return order


class CreateOrder(graphene.Mutation):
    order = graphene.Field(OrderType)

    def mutate(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError("Log in to order a course!")
        email = user.email
        fullName = f"{user.first_name} {user.last_name}"
        phone = user.phone
        address = user.address
        last_order = Order.objects.filter(email=email).last()
        if last_order and not last_order.paid:
            return CreateOrder(order=last_order)
        order = Order(full_name=fullName, email=email, phone=phone, address=address)
        order.save()
        return CreateOrder(order=order)


class CreateOrderItem(graphene.Mutation):
    orderItem = graphene.Field(OrderItemType)

    class Arguments:
        courseId = graphene.Int()
        orderId = graphene.Int()
        quantity = graphene.Int()

    def mutate(self, info, courseId, orderId, quantity):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError("Log in to order a course!")
        course = Course.objects.get(pk=courseId)
        order = Order.objects.get(pk=orderId)
        price = course.price
        qs_course = OrderItem.objects.filter(
            course__id=courseId, order__email=user.email
        ).exists()
        if qs_course:
            raise GraphQLError("La formation est deja ajoute au panier")
        order_item = OrderItem(
            course=course, price=price, quantity=quantity, order=order
        )
        order_item.save()
        return CreateOrderItem(orderItem=order_item)


class RemoveOrderItem(graphene.Mutation):
    isDeleted = graphene.Boolean()

    class Arguments:
        orderItemId = graphene.Int()
        orderId = graphene.Int()

    def mutate(self, info, orderItemId):
        orderItem = OrderItem.objects.get(pk=orderItemId)
        orderItem.delete()
        return RemoveOrderItem(isDeleted=True)


class Mutation(graphene.ObjectType):
    create_order = CreateOrder.Field()
    create_order_item = CreateOrderItem.Field()
    remove_order_item = RemoveOrderItem.Field()