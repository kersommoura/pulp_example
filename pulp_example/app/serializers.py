from rest_framework import serializers
from pulpcore.plugin import serializers as platform

from . import models


class ExampleContentSerializer(platform.ContentSerializer):
    path = serializers.CharField()
    digest = serializers.CharField()

    class Meta:
        fields = platform.ContentSerializer.Meta.fields + ('path', 'digest')
        model = models.ExampleContent


class ExampleFuturesImporterSerializer(platform.ImporterSerializer):
    class Meta:
        fields = platform.ImporterSerializer.Meta.fields
        model = models.ExampleFuturesImporter


class ExampleAsyncIOImporterSerializer(platform.ImporterSerializer):
    class Meta:
        fields = platform.ImporterSerializer.Meta.fields
        model = models.ExampleAsyncIOImporter


class ExamplePublisherSerializer(platform.PublisherSerializer):
    class Meta:
        fields = platform.PublisherSerializer.Meta.fields
        model = models.ExamplePublisher
