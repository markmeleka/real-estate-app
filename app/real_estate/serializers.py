from real_estate.models import Address, Listing
from rest_framework import serializers


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = "__all__"
        read_only_fields = ("id",)


class AddressListSerializer(AddressSerializer):
    class Meta:
        model = Address
        fields = (
            "id",
            "street_address",
            "unit_number",
            "city",
            "state",
            "zipcode",
        )
        read_only_fields = ("id",)


class ListingSerializer(serializers.ModelSerializer):
    address = AddressSerializer(many=False)

    class Meta:
        model = Listing
        fields = "__all__"

        read_only_fields = ("id",)

    def create(self, validated_data):
        address_validated_data = validated_data.pop("address")
        address = Address.objects.get_or_create(**address_validated_data)[0]
        validated_data["address"] = address
        listing = Listing.objects.create(**validated_data)
        return listing


class ListingListSerializer(ListingSerializer):
    address = AddressListSerializer(many=False)

    class Meta:
        model = Listing
        fields = (
            "id",
            "address",
            "listing_number",
            "date_accessed",
            "price",
            "size_interior",
            "bedrooms",
            "num_bathrooms",
            "num_stories",
            "num_units",
            "land_size",
            "property_type",
            "building_type",
            "ownership_type",
            "num_parking",
        )

        read_only_fields = ("id",)
