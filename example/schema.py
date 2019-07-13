"""
Graphene schema for example
Contains Nodes for Actor, CountryOrigin, Moive
Contains Query for specific ID or filtering for all objects
Contains Input for all Nodes
Contains Mutation for all Input
"""
from example.models import Movie, CountryOrigin, Actor
import graphene
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.types import DjangoObjectType
from graphql_relay import from_global_id


class ActorNode(DjangoObjectType):
    '''
    Actor Node represents the model Actor
    '''
    class Meta:
        model = Actor
        interfaces = (graphene.Node,)
        filter_fields = ['id', 'name']


class CountryOriginNode(DjangoObjectType):
    '''
    CountryOrigin Node represents the model CountryOrigin
    '''
    class Meta:
        model = CountryOrigin
        interfaces = (graphene.Node,)
        filter_fields = ['id', 'country']


class MovieNode(DjangoObjectType):
    '''
    Movie Node represents the model Movie
    '''
    class Meta:
        model = Movie
        interfaces = (graphene.Node,)
        filter_fields = [
                         'id',
                         'title',
                         'actors',
                         'country_origin'
                        ]


class Query(graphene.ObjectType):
    '''
    Node definitions of each Model for retrieval by ID.
    Connection definitions for each Model for filtering by model fields
    '''
    moive = graphene.Node.Field(MovieNode)
    all_moives = DjangoFilterConnectionField(MovieNode)

    country_origin = graphene.Node.Field(CountryOriginNode)
    all_country_origin = DjangoFilterConnectionField(CountryOriginNode)

    actor = graphene.Node.Field(ActorNode)
    all_actors = DjangoFilterConnectionField(ActorNode)


# Input classes for mutation
class ActorInput(graphene.InputObjectType):
    '''
    Mutatable inputs for Actor
    '''
    id = graphene.ID()
    name = graphene.String()


class CountryOriginInput(graphene.InputObjectType):
    '''
    Mutatable inputs for CountryOrigin
    '''
    id = graphene.ID()
    country = graphene.String()


class MovieInput(graphene.InputObjectType):
    '''
    Mutatable inputs for Movie
    '''
    id = graphene.ID()
    title = graphene.String()
    actors = graphene.List(ActorInput)
    country_origin = graphene.Field(CountryOriginInput)
    year = graphene.Int()


class CreateActor(graphene.Mutation):
    '''
    A Mutation class for creating an Actor
    '''
    class Arguments:
        '''
        Represents what fields can be passed to the mutate method
        '''
        input = ActorInput(required=True)

    # the return fields for CreateActor
    ok = graphene.Boolean()
    actor = graphene.Field(ActorNode)

    @staticmethod
    def mutate(root, info, input):
        '''
        Overridden mutate method
        Args:
            root (obj): no idea what this is
            info (obj): resolve info
            input (obj): the ActorInput
        Returns:
            obj: the created actor
        '''
        print(root, type(root))
        print(info, type(info))
        ok = True
        instance = Actor(name=input.name)
        instance.save()
        return CreateActor(ok=ok, actor=instance)


class UpdateActor(graphene.Mutation):
    '''
    A Mutation class for updating Actor
    '''
    class Arguments:
        '''
        Represents what fields can be passed to the mutate method
        '''
        id = graphene.ID(required=True)
        input = ActorInput(required=True)

    # the return fields for UpdateActor
    ok = graphene.Boolean()
    actor = graphene.Field(ActorNode)

    @staticmethod
    def mutate(root, info, id, input):
        '''
        Overridden mutate method
        Args:
            root (obj): no idea what this is
            info (obj): resolve info
            id (str): the arg input
            input (obj): the ActorInput
        Returns:
            obj: the updated actor
        '''
        ok = False
        _, actor_pk = from_global_id(id)
        actor_instance = Actor.objects.get(pk=actor_pk)
        if actor_instance:
            ok = True
            instance.name = input.name
            instance.save()
            return UpdateActor(ok=ok, actor=instance)
        return UpdateActor(ok=ok, actor=None)


class CreateCountryOrigin(graphene.Mutation):
    '''
    A Mutation class for creating CountryOrigin
    '''
    class Arguments:
        '''
        Represents what fields can be passed to the mutate method
        '''
        input = CountryOriginInput(required=True)

    # the return fields for CreateCountryOrigin
    ok = graphene.Boolean()
    country_origin = graphene.Field(CountryOriginNode)

    @staticmethod
    def mutate(root, info, input):
        '''
        Overridden mutate method
        Args:
            root (obj): no idea what this is
            info (obj): resolve info
            input (obj): the CountryOriginInput
        Returns:
            obj: the created country_origin
        '''
        ok = True
        instance = CountryOrigin(country=input.country)
        instance.save()
        return CreateCountryOrigin(ok=ok, country_origin=instance)


class UpdateCountryOrigin(graphene.Mutation):
    '''
    A Mutation class for updating CountryOrigin
    '''
    class Arguments:
        '''
        Represents what fields can be passed to the mutate method
        '''
        id = graphene.ID(required=True)
        input = CountryOriginInput(required=True)

    # the return fields for UpdateCountryOrigin
    ok = graphene.Boolean()
    country_origin = graphene.Field(CountryOriginNode)

    @staticmethod
    def mutate(root, info, id, input):
        '''
        Overridden mutate method
        Args:
            root (obj): no idea what this is
            info (obj): resolve info
            id (str): the arg input
            input (obj): the CountryOriginInput
        Returns:
            obj: the updated country_origin
        '''
        ok = False
        _, country_origin_pk = from_global_id(id)
        instance = CountryOrigin.objects.get(pk=country_origin_pk)
        if instance:
            ok = True
            instance.country = input.country
            instance.save()
            return UpdateCountryOrigin(ok=ok, country_origin=instance)
        return UpdateActor(ok=ok, actor=None)


class CreateMovie(graphene.Mutation):
    '''
    A Mutation class for creating Movie
    '''
    class Arguments:
        '''
        Represents what fields can be passed to the mutate method
        '''
        input = MovieInput(required=True)

    # the return fields for CreateMovie
    ok = graphene.Boolean()
    movie = graphene.Field(MovieNode)

    @staticmethod
    def mutate(root, info, input):
        '''
        Overridden mutate method
        Args:
            root (obj): no idea what this is
            info (obj): resolve info
            input (obj): the MoiveInput
        Returns:
            obj: the updated movie
        '''
        ok = True
        actors = []
        country_origin_instance = None

        for actor_input in input.actors:
            # need to decode the global_id to db_id
            _, actor_pk = from_global_id(actor_input.id)
            actor = Actor.objects.get(pk=actor_pk)

            if actor is None:
                return CreateMovie(ok=False, movie=None)
            actors.append(actor)

        if input.country_origin:
            # need to decode the global_id to db_id
            _, country_origin_pk = from_global_id(input.country_origin.id)
            country_origin_instance = CountryOrigin.objects.get(pk=country_origin_pk)

        instance = Movie(
          title=input.title,
          year=input.year,
          country_origin=country_origin_instance
          )
        instance.save()
        instance.actors.set(actors)
        return CreateMovie(ok=ok, movie=instance)


class UpdateMovie(graphene.Mutation):
    '''
    A Mutation class for updating Movie
    '''
    class Arguments:
        '''
        Represents what fields can be passed to the mutate method
        '''
        id = graphene.ID(required=True)
        input = MovieInput(required=True)

    # the return fields for UpdateMovie
    ok = graphene.Boolean()
    movie = graphene.Field(MovieNode)

    @staticmethod
    def mutate(root, info, id, input):
        '''
        Overridden mutate method
        Args:
            root (obj): no idea what this is
            info (obj): resolve info
            id (str): the arg input
            input (obj): the MoiveInput
        Returns:
            obj: the updated movie
        '''
        ok = False

        # need to decode the global_id to db_id
        _, movie_pk = from_global_id(id)
        instance = Movie.objects.get(pk=movie_pk)

        if instance:
            ok = True
            actors = []

            if input.actors:
                for actor_input in input.actors:
                    # need to decode the global_id to db_id
                    _, actor_pk = from_global_id(actor_input.id)
                    actor = Actor.objects.get(pk=actor_pk)
                    if actor is None:
                        return UpdateMovie(ok=False, movie=None)
                    actors.append(actor)
            elif instance.actors:
                actors = instance.actors

            for key, val in input.items():
                if key == 'actors' or key == 'country_origin':
                    continue
                # only update values that are passed in input
                setattr(instance, key, val)

            if input.country_origin:
                # need to decode the global_id to db_id
                _, country_origin_pk = from_global_id(input.country_origin.id)
                country_origin = CountryOrigin.objects.get(pk=country_origin_pk)
                if country_origin:
                    instance.country_origin = country_origin

            instance.save()
            instance.actors.set(actors)
            return UpdateMovie(ok=ok, movie=instance)
        return UpdateMovie(ok=ok, movie=None)


class Mutation(graphene.ObjectType):
    '''
    Create definitions for Mutation
    Update definitions for Mutation
    '''
    create_actor = CreateActor.Field()
    update_actor = UpdateActor.Field()

    create_country_origin = CreateCountryOrigin.Field()
    update_country_origin = UpdateCountryOrigin.Field()

    create_movie = CreateMovie.Field()
    update_movie = UpdateMovie.Field()
