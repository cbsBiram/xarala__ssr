import graphene
import users.schema
import course.schema
import blog.schema
import quiz.schema
import pages.schema
import cart.schema


class Query(
    users.schema.Query,
    course.schema.Query,
    blog.schema.Query,
    quiz.schema.Query,
    graphene.ObjectType,
):
    pass


class Mutation(
    blog.schema.Mutation,
    course.schema.Mutation,
    pages.schema.Mutation,
    quiz.schema.Mutation,
    users.schema.Mutation,
    cart.schema.Mutation,
):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
