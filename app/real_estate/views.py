from real_estate import serializers
from real_estate.models import Address, Listing
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated


class AddressViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.AddressSerializer
    queryset = Address.objects.all()

    def get_serializer_class(self):
        if self.action in ["list"]:
            return serializers.AddressListSerializer
        else:
            return serializers.AddressSerializer


class ListingViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.ListingSerializer
    queryset = Listing.objects.all()

    def get_serializer_class(self):
        if self.action in ["list"]:
            return serializers.ListingListSerializer
        else:
            return serializers.ListingSerializer
