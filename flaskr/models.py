from py2neo import Graph
from flaskr import settings
from py2neo.ogm import GraphObject, Property, RelatedFrom, RelatedTo

graph = Graph(
    host=settings.NEO4J_HOST,
    port=settings.NEO4J_PORT,
    user=settings.NEO4J_USER,
    password=settings.NEO4J_HOST
)


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


class Tweet(BaseModel): 

    content = Property()

    user = RelatedTo('User', 'TWEETED')


class User(BaseModel):

    username = Property()
    passwordHash = Property()
    salt = Property()

    subscribedUsers = RelatedTo('User', 'FOLLOWS')
    

