"""
Main Graphene Schema
"""

import example.schema as example
import graphene

from graphene_django.debug import DjangoDebug


class Query(
    example.Query,
    graphene.ObjectType
):
    debug = graphene.Field(DjangoDebug, name='_debug')


class Mutation(
    example.Mutation,
    graphene.ObjectType
):
    debug = graphene.Field(DjangoDebug, name='_debug')

schema = graphene.Schema(query=Query, mutation=Mutation)
