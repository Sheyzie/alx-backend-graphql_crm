import graphene


class CRMQuery(graphene.ObjectType):
    hello = graphene.String()

    def resolve_name(self, info):
        return "Hello, GraphQL!"

