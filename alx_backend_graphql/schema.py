import graphene


class Query(graphene.ObjectType):
    hello = graphene.String()

    def resolve_name(self, info):
        return "Hello, GraphQL!"
    

schema = graphene.Schema(query=Query)