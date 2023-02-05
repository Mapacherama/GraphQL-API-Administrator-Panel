import os
from dotenv import load_dotenv

from django.contrib.auth import get_user_model, authenticate, login
import graphene
from graphene import ObjectType, String, Int, InputObjectType, Mutation, Field
from graphene_django import DjangoObjectType
from graphql_jwt.decorators import login_required, permission_required
from graphene_file_upload.scalars import Upload
from graphql import GraphQLError

import graphql_jwt

from graphql_jwt.shortcuts import create_refresh_token, get_token

load_dotenv()

class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()
        fields = ["id", "email", "username", "first_name", "last_name"]

class Query(ObjectType):
    user = Field(UserType, id=Int(required=True))
    who_am_i = graphene.Field(UserType)

    @login_required
    def resolve_who_am_i(self, info):
        return info.context.user

    def resolve_hello(self, info, name):
        return 'Hello ' + name

    def resolve_user(self, info, id):
        return get_user_model().objects.get(id=id)

class CreateUser(Mutation):
    user = graphene.Field(UserType)
    token = graphene.String()
    refresh_token = graphene.String()

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



class LoginUser(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)

    success = graphene.Boolean()

    def mutate(self, info, username, password):
        user = authenticate(username=username, password=password)
        if user is None:
            raise GraphQLError("Invalid username or password.")
        login(info.context, user)
        return LoginUser(success=True)        

class Mutation(ObjectType):
    upload_file = Field(Upload, file=Upload(required=True))
    create_user = CreateUser.Field()
    login = LoginUser.Field()
    
    # Create and alter tokens
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    revoke_token = graphql_jwt.Revoke.Field()
    delete_token_cookie = graphql_jwt.DeleteJSONWebTokenCookie.Field()
    delete_refresh_token_cookie = graphql_jwt.DeleteRefreshTokenCookie.Field()