from django_filters import rest_framework as filters
from rest_framework_bulk.serializers import BulkListSerializer, BulkSerializerMixin

from .api.serializers import ModelSerializer
from .api.views import (
    frePPleListCreateAPIView,
    frePPleRetrieveUpdateDestroyAPIView,
)

from . import models


class BucketFilter(filters.FilterSet):
    class Meta:
        model = models.Bucket
        fields = {
            "name": ["exact", "in", "contains"],
            "description": ["exact", "contains"],
            "level": ["exact", "in", "gt", "gte", "lt", "lte"],
            "source": ["exact", "in"],
            "lastmodified": ["exact", "in", "gt", "gte", "lt", "lte"],
        }
        filter_fields = ("name", "description", "level")


class BucketSerializer(BulkSerializerMixin, ModelSerializer):
    class Meta:
        model = models.Bucket
        fields = ("name", "description", "level", "source", "lastmodified")
        list_serializer_class = BulkListSerializer
        update_lookup_field = "name"
        partial = True


class BucketAPI(frePPleListCreateAPIView):
    queryset = models.Bucket.objects.all()
    serializer_class = BucketSerializer
    filter_class = BucketFilter


class BucketDetailFilter(filters.FilterSet):
    class Meta:
        model = models.BucketDetail
        fields = {
            "bucket": ["exact", "in"],
            "name": ["exact", "in", "contains"],
            "startdate": ["exact", "in", "gt", "gte", "lt", "lte"],
            "enddate": ["exact", "in", "gt", "gte", "lt", "lte"],
            "source": ["exact", "in"],
            "lastmodified": ["exact", "in", "gt", "gte", "lt", "lte"],
        }
        filter_fields = (
            "bucket",
            "name",
            "startdate",
            "enddate",
            "source",
            "lastmodified",
        )


class BucketdetailAPI(frePPleRetrieveUpdateDestroyAPIView):
    queryset = models.Bucket.objects.all()
    serializer_class = BucketSerializer
    filter_class = BucketFilter


class BucketDetailSerializer(BulkSerializerMixin, ModelSerializer):
    class Meta:
        model = models.BucketDetail
        fields = ("bucket", "name", "startdate", "enddate", "source", "lastmodified")


class BucketDetailAPI(frePPleListCreateAPIView):
    queryset = models.BucketDetail.objects.all()
    serializer_class = BucketDetailSerializer
    filter_class = BucketDetailFilter


class BucketDetaildetailAPI(frePPleRetrieveUpdateDestroyAPIView):
    queryset = models.BucketDetail.objects.all()
    serializer_class = BucketDetailSerializer
    filter_class = BucketDetailFilter


class CommentSerializer(BulkSerializerMixin, ModelSerializer):
    class Meta:
        model = models.Comment
        fields = ("id", "object_pk", "comment", "lastmodified", "content_type", "user")
        list_serializer_class = BulkListSerializer
        update_lookup_field = "id"
        partial = True


class CommentAPI(frePPleListCreateAPIView):
    queryset = models.Comment.objects.all()
    serializer_class = CommentSerializer
    filter_fields = (
        "id",
        "object_pk",
        "comment",
        "lastmodified",
        "content_type",
        "user",
    )


class CommentdetailAPI(frePPleRetrieveUpdateDestroyAPIView):
    queryset = models.Comment.objects.all()
    serializer_class = CommentSerializer


class ParameterFilter(filters.FilterSet):
    class Meta:
        model = models.Parameter
        fields = {
            "name": ["exact", "in", "contains"],
            "description": ["exact", "contains"],
            "value": ["exact", "in", "contains"],
            "source": ["exact", "in"],
            "lastmodified": ["exact", "in", "gt", "gte", "lt", "lte"],
        }
        filter_fields = ("name", "value", "description", "source", "lastmodified")


class ParameterSerializer(BulkSerializerMixin, ModelSerializer):
    class Meta:
        model = models.Parameter
        fields = ("name", "source", "lastmodified", "value", "description")
        list_serializer_class = BulkListSerializer
        update_lookup_field = "name"
        partial = True


class ParameterAPI(frePPleListCreateAPIView):
    queryset = models.Parameter.objects.all()
    serializer_class = ParameterSerializer
    filter_class = ParameterFilter


class ParameterdetailAPI(frePPleRetrieveUpdateDestroyAPIView):
    queryset = models.Parameter.objects.all()
    serializer_class = ParameterSerializer
    filter_class = ParameterFilter
