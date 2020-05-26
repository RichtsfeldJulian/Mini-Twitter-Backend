from py2neo import Graph, NodeMatcher, Relationship
from flaskr import settings
from py2neo.ogm import GraphObject, Property, RelatedFrom, RelatedTo
from graphql import GraphQLError

graph = Graph(user=settings.NEO4J_USER, password=settings.NEO4J_PASSWORD)
matcher = NodeMatcher(graph)

class BaseModel(GraphObject):
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    @property
    def all(self):
        return self.match(graph)

    def save(self):
        graph.push(self)

    def delete(self):
        graph.delete(self)



class Tweet(BaseModel): 

    content = Property()

    user = RelatedFrom('User', 'TWEETED')

    def addUser(self, username):
        user = User(username=username).fetch()
        if user is None:
            raise GraphQLError("User was not found")
        self.user.add(user)



class User(BaseModel):
    __primarykey__ = "username"

    username = Property()
    passwordHash = Property()

    subscribedUsers = RelatedTo('User', 'FOLLOWS')

    def fetch(self):
        return self.match(graph, self.username).first()



