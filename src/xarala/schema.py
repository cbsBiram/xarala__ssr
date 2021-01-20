import graphene
import graphql_jwt
import users.schema
import course.schema
import blog.schema
import quiz.schema


class Query(
    users.schema.Query,
    course.schema.Query,
    blog.schema.Query,
    quiz.schema.Query,
    graphene.ObjectType,
):
    pass


class Mutation(
    users.schema.Mutation,
    course.schema.Mutation,
    quiz.schema.Mutation,
    blog.schema.Mutation,
    graphene.ObjectType,
):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
