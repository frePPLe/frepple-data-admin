from django_filters import rest_framework as filters
from rest_framework_bulk.drf3.serializers import BulkListSerializer, BulkSerializerMixin

from data_admin.common.api.views import (
    frePPleListCreateAPIView,
    frePPleRetrieveUpdateDestroyAPIView,
)
from . import models
from data_admin.common.api.serializers import ModelSerializer

import logging

logger = logging.getLogger(__name__)


class LocationFilter(filters.FilterSet):
    class Meta:
        model = models.Location
        fields = {
            "name": ["exact", "in", "contains"],
            "owner": ["exact", "in"],
            "description": ["exact", "in", "contains"],
            "category": ["exact", "in", "contains"],
            "subcategory": ["exact", "in", "contains"],
            "source": ["exact", "in"],
            "lastmodified": ["exact", "in", "gt", "gte", "lt", "lte"],
        }
        filter_fields = (
            "name",
            "owner",
            "description",
            "category",
            "subcategory",
            "source",
            "lastmodified",
        )


class LocationSerializer(BulkSerializerMixin, ModelSerializer):
    class Meta:
        model = models.Location
        fields = (
            "name",
            "owner",
            "description",
            "category",
            "subcategory",
            "source",
            "lastmodified",
        )
        list_serializer_class = BulkListSerializer
        update_lookup_field = "name"
        partial = True


class LocationAPI(frePPleListCreateAPIView):
    queryset = models.Location.objects.all()
    serializer_class = LocationSerializer
    filter_class = LocationFilter


class LocationdetailAPI(frePPleRetrieveUpdateDestroyAPIView):
    queryset = models.Location.objects.all()
    serializer_class = LocationSerializer


class CustomerFilter(filters.FilterSet):
    class Meta:
        model = models.Customer
        fields = {
            "name": ["exact", "in", "contains"],
            "owner": ["exact", "in"],
            "description": ["exact", "in", "contains"],
            "category": ["exact", "in", "contains"],
            "subcategory": ["exact", "in", "contains"],
            "source": ["exact", "in"],
            "lastmodified": ["exact", "in", "gt", "gte", "lt", "lte"],
        }
        filter_fields = (
            "name",
            "owner",
            "description",
            "category",
            "subcategory",
            "source",
            "lastmodified",
        )


class CustomerSerializer(BulkSerializerMixin, ModelSerializer):
    class Meta:
        model = models.Customer
        fields = (
            "name",
            "owner",
            "description",
            "category",
            "subcategory",
            "source",
            "lastmodified",
        )
        list_serializer_class = BulkListSerializer
        update_lookup_field = "name"
        partial = True


class CustomerAPI(frePPleListCreateAPIView):
    queryset = models.Customer.objects.all()
    serializer_class = CustomerSerializer
    filter_class = CustomerFilter


class CustomerdetailAPI(frePPleRetrieveUpdateDestroyAPIView):
    queryset = models.Customer.objects.all()
    serializer_class = CustomerSerializer


class ItemFilter(filters.FilterSet):
    class Meta:
        model = models.Item
        fields = {
            "name": ["exact", "in", "contains"],
            "owner": ["exact", "in"],
            "description": ["exact", "in", "contains"],
            "category": ["exact", "in", "contains"],
            "subcategory": ["exact", "in", "contains"],
            "cost": ["exact", "in", "gt", "gte", "lt", "lte"],
            "volume": ["exact", "in", "gt", "gte", "lt", "lte"],
            "weight": ["exact", "in", "gt", "gte", "lt", "lte"],
            "type": ["exact", "in"],
            "source": ["exact", "in"],
            "lastmodified": ["exact", "in", "gt", "gte", "lt", "lte"],
        }
        filter_fields = (
            "name",
            "owner",
            "description",
            "category",
            "subcategory",
            "cost",
            "weight",
            "volume",
            "type",
            "source",
            "lastmodified",
        )


class ItemSerializer(BulkSerializerMixin, ModelSerializer):
    class Meta:
        model = models.Item
        fields = (
            "name",
            "owner",
            "description",
            "category",
            "subcategory",
            "cost",
            "volume",
            "weight",
            "type",
            "source",
            "lastmodified",
        )
        list_serializer_class = BulkListSerializer
        update_lookup_field = "name"
        partial = True


class ItemAPI(frePPleListCreateAPIView):
    queryset = models.Item.objects.all()
    serializer_class = ItemSerializer
    filter_class = ItemFilter


class ItemdetailAPI(frePPleRetrieveUpdateDestroyAPIView):
    queryset = models.Item.objects.all()
    serializer_class = ItemSerializer


class DemandFilter(filters.FilterSet):
    class Meta:
        model = models.Demand
        fields = {
            "name": ["exact", "in", "contains"],
            "description": ["exact", "in", "contains"],
            "category": ["exact", "in", "contains"],
            "subcategory": ["exact", "in", "contains"],
            "item": ["exact", "in"],
            "customer": ["exact", "in"],
            "location": ["exact", "in"],
            "due": ["exact", "in", "gt", "gte", "lt", "lte"],
            "status": ["exact", "in"],
            "quantity": ["exact", "in", "gt", "gte", "lt", "lte"],
        }

        filter_fields = (
            "name",
            "description",
            "category",
            "subcategory",
            "item",
            "customer",
            "location",
            "due",
            "status",
            "quantity",
        )


class DemandSerializer(BulkSerializerMixin, ModelSerializer):
    class Meta:
        model = models.Demand
        fields = (
            "name",
            "description",
            "category",
            "subcategory",
            "item",
            "customer",
            "location",
            "due",
            "status",
            "quantity",
        )
        list_serializer_class = BulkListSerializer
        update_lookup_field = "name"
        partial = True


class DemandAPI(frePPleListCreateAPIView):
    queryset = models.Demand.objects.all()
    serializer_class = DemandSerializer
    filter_class = DemandFilter


class DemanddetailAPI(frePPleRetrieveUpdateDestroyAPIView):
    queryset = models.Demand.objects.all()
    serializer_class = DemandSerializer
