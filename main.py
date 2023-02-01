import os
import psycopg2
from dotenv import load_dotenv
import json

import graphene
from flask import Flask
from flask_graphql import GraphQLView
from graphene_file_upload.scalars import Upload

import administrator.user_type

user_module = administrator.user_type.UserType

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

class UserInputType(graphene.InputObjectType):
    class Meta:
        fields = ('id', 'username', 'email', 'password')


class Query(graphene.ObjectType):
    hello = graphene.String(name=graphene.String(default_value="stranger"))

    def resolve_hello(self, info, name, conn=conn):
        return 'Hello ' + name

class Query(graphene.ObjectType):
    user = graphene.Field(user_module, id=graphene.Int(required=True))

    def resolve_user(self, info, id):
        # Implement code to retrieve user data based on the id
        user =  resolve_user(id)
        return user

def resolve_user(self, info, id):
# Create a cursor for executing SQL commands
    cursor = conn.cursor()

    # Execute a SQL query to retrieve the user with the specified id
    cursor.execute("SELECT * FROM users WHERE id=%s", (id,))

    # Fetch the user data
    user_data = cursor.fetchone()

    # Close the cursor and the database connection
    cursor.close()
    conn.close()

    # Return the user data
    return user_module(
        id=user_data[0],
        username=user_data[1],
        email=user_data[2],
        password=user_data[3]
    )            


class Mutation(graphene.ObjectType):
    upload_file = graphene.Field(Upload, file=Upload(required=True))

class CreateUser(graphene.Mutation):
    class Arguments:
        input = UserInputType(required=True)
    
    user = graphene.Field(user_module, id = graphene.Int(required=True))
    
    def mutate(self, info, input):
        user = UserType(
            username=input['username'],
            password=input['password'],
            email=input['email']
        )
        user.save()
        return CreateUser(user=user)


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
