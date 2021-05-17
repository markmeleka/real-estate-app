from django_filters.rest_framework import (
    CharFilter,
    DateFilter,
    FilterSet,
    NumberFilter,
)
from real_estate import serializers
from real_estate.models import Address, Listing
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated


class AddressFilter(FilterSet):
    min_latitude = NumberFilter(field_name="latitude", lookup_expr="gte")
    max_latitude = NumberFilter(field_name="latitude", lookup_expr="lte")
    min_longitude = NumberFilter(field_name="longitude", lookup_expr="gte")
    max_longitude = NumberFilter(field_name="longitude", lookup_expr="lte")

    class Meta:
        model = Address
        fields = {
            "id": ["exact"],
            "street_address": ["exact"],
            "unit_number": ["exact"],
            "city": ["exact"],
            "state": ["exact"],
            "zipcode": ["exact", "icontains"],
            "country": ["exact"],
        }


class AddressViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.AddressSerializer
    queryset = Address.objects.all()
    filterset_class = AddressFilter

    def get_serializer_class(self):
        if self.action in ["list"]:
            return serializers.AddressListSerializer
        else:
            return serializers.AddressSerializer


class ListingFilter(FilterSet):
    address_id = NumberFilter(field_name="address__id", lookup_expr="exact")
    street_address = CharFilter(
        field_name="address__street_address", lookup_expr="iexact"
    )
    city = CharFilter(field_name="address__city", lookup_expr="iexact")
    state = CharFilter(field_name="address__state", lookup_expr="iexact")
    zipcode = CharFilter(field_name="address__zipcode", lookup_expr="iexact")
    zipcode_contains = CharFilter(
        field_name="address__zipcode", lookup_expr="icontains"
    )
    country = CharFilter(field_name="address__country", lookup_expr="iexact")
    listing_number = CharFilter(
        field_name="listing_number", lookup_expr="iexact"
    )
    min_date = DateFilter(field_name="date_accessed", lookup_expr="gte")
    max_date = DateFilter(field_name="date_accessed", lookup_expr="lte")
    min_price = NumberFilter(field_name="price", lookup_expr="gte")
    max_price = NumberFilter(field_name="price", lookup_expr="lte")
    min_size_interior = CharFilter(
        field_name="size_interior", lookup_expr="gte"
    )
    min_bedrooms = CharFilter(field_name="bedrooms", lookup_expr="gte")
    min_bathrooms = NumberFilter(field_name="num_bathrooms", lookup_expr="gte")
    min_units = NumberFilter(field_name="num_units", lookup_expr="gte")
    ownership_type = CharFilter(
        field_name="ownership_type", lookup_expr="iexact"
    )
    min_parking = NumberFilter(field_name="num_parking", lookup_expr="gte")
    description = CharFilter(field_name="description", lookup_expr="icontains")


class ListingViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.ListingSerializer
    queryset = Listing.objects.all()
    filterset_class = ListingFilter

    def get_serializer_class(self):
        if self.action in ["list"]:
            return serializers.ListingListSerializer
        else:
            return serializers.ListingSerializer
