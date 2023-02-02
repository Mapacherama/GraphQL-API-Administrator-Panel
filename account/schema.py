import os
from dotenv import load_dotenv

from django.contrib.auth import get_user_model
import graphene
from graphene import ObjectType, String, Int, InputObjectType, Mutation, Field
from graphene_django import DjangoObjectType
from graphene_file_upload.scalars import Upload

from graphql_jwt.shortcuts import create_refresh_token, get_token

load_dotenv()

class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()
        fields = ["id", "email", "username", "first_name", "last_name"]

class Query(ObjectType):
    user = Field(UserType, id=Int(required=True))

    def resolve_hello(self, info, name):
        return 'Hello ' + name

    def resolve_user(self, info, id):
        return get_user_model().objects.get(id=id)

class CreateUser(Mutation):
    user = graphene.Field(UserType)
    token = graphene.String()
    refresh_token = graphene.String()

    #     email = models.EmailField(unique=True)
    # username = models.CharField(max_length=30, unique=True)
    # first_name = models.CharField(max_length=30)
    # last_name = models.CharField(max_length=30)
    # phone_nr = models.CharField(max_length=15)
    # password = models.CharField(max_length=64)

    # def set_password(self, raw_password):
    #     self.password = make_password(raw_password)

    # gender = models.CharField(max_length=10, choices=Gender.choices, default=Gender.MALE)
    # spoken_languages = models.CharField(max_length=255, choices=LanguageEnum.choices, default = LanguageEnum.ENGLISH)

    class Arguments:
        email = graphene.String(required=True)
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)
        phone_nr = graphene.String(required=True)
        gender = graphene.String(required=True)
        spoken_languages = graphene.String(required=True)


    user = Field(UserType)

    def mutate(self, info, email, password, first_name, last_name, phone_nr, gender, spoken_languages):
        user = get_user_model()(email = email)
        user.set_password(password)
        user.first_name = first_name
        user.last_name = last_name
        user.gender = gender
        user.phone_nr = phone_nr
        user.spoken_languages = spoken_languages        
        user.save()

        token = get_token(user)
        refresh_token = create_refresh_token(user)

        return CreateUser(user=user, token = token, refresh_token = refresh_token)

class Mutation(ObjectType):
    upload_file = Field(Upload, file=Upload(required=True))
    create_user = CreateUser.Field()