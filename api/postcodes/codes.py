from rest_framework.viewsets import ModelViewSet
from postcodes.models import Code
from postcodes.serializers import CodeSerializer


class PostCodeAPIView(ModelViewSet):
    model = Code
    serializer_class = CodeSerializer
    queryset = model.objects.all()
    http_method_names = ['post', 'get']

    def get_queryset(self):
        return self.model.objects.filter(postcode=self.request.query_params['postcode'])
