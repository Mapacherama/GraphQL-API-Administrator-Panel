import graphene
from .conversions import convert_to_phonenumber
from .user_enums import GenderEnum, LanguageEnum

class UserType(graphene.ObjectType):
    id = graphene.ID()
    email = graphene.String()
    username = graphene.String()
    first_name = graphene.String()
    last_name = graphene.String()
    phone_nr = graphene.String()
    gender = graphene.Field(GenderEnum)
    spoken_languages = graphene.List(LanguageEnum, required=True)
    old_password = graphene.String(required=True)
    password = graphene.String(required=True)
    password_verification = graphene.String(required=True)   