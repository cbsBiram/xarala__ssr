import graphene
import blog.schema
import course.schema
import orders.schema
import pages.schema
import quiz.schema
import search.schema
import users.schema
import userlogs.schema


class Query(
    blog.schema.Query,
    course.schema.Query,
    quiz.schema.Query,
    orders.schema.Query,
    search.schema.Query,
    users.schema.Query,
    userlogs.schema.Query,
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
