import graphene

class LanguageEnum(graphene.Enum):
    ENGLISH = "EN"
    SPANISH = "ES"
    DUTCH = "NL"

class GenderEnum(graphene.Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"
    OTHER = "OTHER"    