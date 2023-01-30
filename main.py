import graphene
from graphene_file_upload.scalars import Upload
import os
from dotenv import load_dotenv

load_dotenv()

class Query(graphene.ObjectType):
    hello = graphene.String(name=graphene.String(default_value="stranger"))

    def resolve_hello(self, info, name):
        return 'Hello ' + name

class Mutation(graphene.ObjectType):
    upload_file = graphene.Field(Upload, file=Upload(required=True))

schema = graphene.Schema(query=Query, mutation=Mutation)

from flask import Flask
from flask_graphql import GraphQLView

app = Flask(__name__)

app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=graphene.Schema(query=Query),
        graphiql=True  # for having the GraphiQL interface
    )
)

if __name__ == '__main__':
    app.run()