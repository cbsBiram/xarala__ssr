import graphene
import users.schema
import course.schema
import blog.schema
import quiz.schema
import pages.schema
import orders.schema


class Query(
    users.schema.Query,
    course.schema.Query,
    blog.schema.Query,
    quiz.schema.Query,
    orders.schema.Query,
    graphene.ObjectType,
):
    pass


class Mutation(
    blog.schema.Mutation,
    course.schema.Mutation,
    pages.schema.Mutation,
    quiz.schema.Mutation,
    users.schema.Mutation,
    orders.schema.Mutation,
):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
