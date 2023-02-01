import os
import psycopg2
from dotenv import load_dotenv

import graphene
from flask import Flask
from flask_graphql import GraphQLView
from graphene_file_upload.scalars import Upload

import administrator.user_type as user_type
import administrator.user_enums as user_enums

UserType = user_type.UserType
GenderEnum = user_enums.GenderEnum
LanguageEnum = user_enums.LanguageEnum

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
    email = graphene.String()
    username = graphene.String()
    password = graphene.String(required=True)


class Query(graphene.ObjectType):
    hello = graphene.String(name=graphene.String(default_value="stranger"))
    user = graphene.Field(UserType, id=graphene.Int(required=True))

    def resolve_hello(self, info, name):
        return 'Hello ' + name

    def resolve_user(self, info, id):
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id=%s", (id,))
        user_data = cursor.fetchone()
        cursor.close()
        conn.close()
        return UserType(
            id=user_data[0],
            username=user_data[1],
            email=user_data[2],
            password=user_data[3]
        )


class CreateUser(graphene.Mutation):
    class Arguments:
        input = UserInputType(required=True)

    user = graphene.Field(UserType)

    def mutate(self, info, input):
        user = UserType(
            username=input.username,
            password=input.password,
            email=input.email
        )
        user.save()
        return CreateUser(user=user)


class Mutation(graphene.ObjectType):
    upload_file = graphene.Field(Upload, file=Upload(required=True))
    create_user = graphene.Field(CreateUser.Field())


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
