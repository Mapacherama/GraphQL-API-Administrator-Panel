import os
import psycopg2
from dotenv import load_dotenv

import graphene
from flask import Flask
from flask_graphql import GraphQLView
from graphene_file_upload.scalars import Upload

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")

conn = psycopg2.connect(
    host=DB_HOST,
    database=DB_NAME,
    user=DB_USER,
    password=DB_PASS
)

class Query(graphene.ObjectType):
    hello = graphene.String(name=graphene.String(default_value="stranger"))

    def resolve_hello(self, info, name, conn=conn):
        return 'Hello ' + name

class Mutation(graphene.ObjectType):
    upload_file = graphene.Field(Upload, file=Upload(required=True))

schema = graphene.Schema(query=Query, mutation=Mutation)

app = Flask(__name__)

app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True
    )
)

if __name__ == '__main__':
    app.run()
