import graphene
from flask_graphql_auth import (
    AuthInfoField,
    GraphQLAuth,
    get_jwt_identity,
    get_raw_jwt,
    create_access_token,
    create_refresh_token,
    query_jwt_required,
    mutation_jwt_refresh_token_required,
    mutation_jwt_required,
)
import app
from flask_bcrypt import Bcrypt
from flaskr.models import User

class Tweet(graphene.ObjectType):
    content = graphene.String()

class TweetProtected(graphene.Union):
    class Meta:
        types = (Tweet, AuthInfoField)

    @classmethod
    def resolve_type(cls, instance, info):
        return type(instance)


class AuthMutation(graphene.Mutation):
    class Arguments(object):
        username = graphene.String(required=True)
        password = graphene.String(required=True)

    ok = graphene.Boolean()
    access_token = graphene.String()

    @classmethod
    def mutate(cls, _, info, username, password):
        user = User(username=username).fetch()
        if user is None:
            return AuthMutation(ok=False)
        if not (app.becrypt.check_password_hash(user.passwordHash, password)):
            return AuthMutation(ok=False)
        return AuthMutation(access_token=create_access_token(user.username), ok= True)


class RegisterMutation(graphene.Mutation):
    class Arguments(object):
        username = graphene.String(required=True)
        password = graphene.String(required=True)
    
    ok = graphene.Boolean()
    access_token = graphene.String()

    @classmethod
    def mutate(cls, _, info, username, password):
        if User(username=username).fetch() is not None:
            return RegisterMutation(ok=False)
        pwhash = app.becrypt.generate_password_hash(password)
        user = User(username=username, passwordHash=pwhash)
        user.save()
        return RegisterMutation(ok=True, access_token=create_access_token(user.username))

class Query(graphene.ObjectType): 
    tweets = graphene.Field(type=TweetProtected, token=graphene.String())

    @classmethod
    @query_jwt_required
    def resolve_tweets(self, info, token):
        return Tweet(content="Successfully ran query")

class Mutation(graphene.ObjectType): 
    auth = AuthMutation.Field()
    register = RegisterMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)