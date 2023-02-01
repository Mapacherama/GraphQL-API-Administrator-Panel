import os
from dotenv import load_dotenv

from django.contrib.auth import get_user_model
from django.conf import settings
from graphene import ObjectType, String, Int, InputObjectType, Mutation, Field
from graphene_django import DjangoObjectType
from graphene_file_upload.scalars import Upload


load_dotenv()


class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()
        fields = ["id", "email", "username", "first_name", "last_name"]

class UserInputType(InputObjectType):
    email = String()
    username = String()
    password = String(required=True)

class Query(ObjectType):
    user = Field(UserType, id=Int(required=True))

    def resolve_hello(self, info, name):
        return 'Hello ' + name

    def resolve_user(self, info, id):
        return get_user_model().objects.get(id=id)

class CreateUser(Mutation):
    class Arguments:
        input = UserInputType(required=True)

    user = Field(UserType)

    def mutate(self, info, input):
        user = UserType(
            username=input.username,
            password=input.password,
            email=input.email
        )
        user.save()
        return CreateUser(user=user)

class Mutation(ObjectType):
    upload_file = Field(Upload, file=Upload(required=True))
    create_user = Field(CreateUser)