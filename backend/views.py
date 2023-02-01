from django.http import QueryDict
from graphene_django.views import GraphQLView

class PrivateGraphQLView(GraphQLView):
    def parse_body(self, request):
        if isinstance(request, QueryDict):
            return request.dict()
        return super().parse_body(request)

def graphql_view(request, *args, **kwargs):
    kwargs['middleware'] = [
        'graphene_file_upload.middleware.UploadMiddleware',
    ]
    return PrivateGraphQLView.as_view(**kwargs)(request, *args, **kwargs)