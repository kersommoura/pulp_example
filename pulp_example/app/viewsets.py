from django_filters.rest_framework import filterset
from pulpcore.plugin import viewsets as platform

from . import models, serializers


class ExampleContentFilter(filterset.FilterSet):
    class Meta:
        model = models.ExampleContent
        fields = ['path', 'digest']


class ExampleContentViewSet(platform.ContentViewSet):
    endpoint_name = 'example'
    queryset = models.ExampleContent.objects.all()
    serializer_class = serializers.ExampleContentSerializer
    filter_class = ExampleContentFilter


class ExampleFuturesImporterViewSet(platform.ImporterViewSet):
    endpoint_name = 'example-futures'
    queryset = models.ExampleFuturesImporter.objects.all()
    serializer_class = serializers.ExampleFuturesImporterSerializer


class ExampleAsyncIOImporterViewSet(platform.ImporterViewSet):
    endpoint_name = 'example-asyncio'
    queryset = models.ExampleAsyncIOImporter.objects.all()
    serializer_class = serializers.ExampleAsyncIOImporterSerializer


class ExamplePublisherViewSet(platform.PublisherViewSet):
    endpoint_name = 'example'
    queryset = models.ExamplePublisher.objects.all()
    serializer_class = serializers.ExamplePublisherSerializer
