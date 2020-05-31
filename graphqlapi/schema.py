
from graphene import ObjectType, Schema

from api.schema import Query , Mutation

import graphql_jwt


class Query(Query, ObjectType):
    pass

class Mutation(Mutation, ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()

schema = Schema(query=Query,mutation=Mutation)