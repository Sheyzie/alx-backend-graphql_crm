import graphene
from crm.schema import CRMQuery


class Query(CRMQuery, graphene.ObjectType):
    pass
    

schema = graphene.Schema(query=Query)