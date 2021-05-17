import csv

from django.conf import settings
from django.core.management.base import BaseCommand
from real_estate.models import Address, Listing


class Command(BaseCommand):
    help = "Ingests data parsed from realtor.ca"

    def add_arguments(self, parser):
        parser.add_argument(
            "csv_file_name",
            help="Relative path from media root.",
            type=str,
        )

    def handle(self, *args, csv_file_name, **kwargs):
        csv_file_path = f"{settings.MEDIA_ROOT}{csv_file_name}"

        address_mapper = {
            "Property.Address.StreetAddress": "street_address",
            "Property.Address.UnitNumber": "unit_number",
            "Property.Address.City": "city",
            "Property.Address.Province": "state",
            "PostalCode": "zipcode",
            "Property.Address.Country": "country",
            "Property.Address.Latitude": "latitude",
            "Property.Address.Longitude": "longitude",
        }
        listing_mapper = {
            "MlsNumber": "listing_number",
            "DateAccessed": "date_accessed",
            "Property.PriceUnformattedValue": "price",
            "DetailsURL": "details_url",
            "Building.SizeInterior": "size_interior",
            "Building.Bedrooms": "bedrooms",
            "Building.BathroomTotal": "num_bathrooms",
            "Building.StoriesTotal": "num_stories",
            "Building.UnitTotal": "num_units",
            "Land.SizeTotal": "land_size",
            "Land.SizeFrontage": "frontage",
            "Property.PhotoLink": "photo_link",
            "Property.Type": "property_type",
            "Building.Type": "building_type",
            "Property.OwnershipType": "ownership_type",
            "Property.Parking": "parking_type",
            "Property.ParkingSpaceTotal": "num_parking",
            "PublicRemarks": "description",
        }
        file_mapper = {**address_mapper, **listing_mapper}

        with open(csv_file_path) as data:
            reader = csv.reader(data, delimiter=",")
            header = next(reader)
            header = [
                file_mapper[h] if h in file_mapper else h for h in header
            ]
            for row in reader:
                row_dict = dict(zip(header, row))
                address_object_dict = {
                    k: row_dict[k]
                    for k in row_dict
                    if k in address_mapper.values() and row_dict[k]
                }
                listing_object_dict = {
                    k: row_dict[k]
                    for k in row_dict
                    if k in listing_mapper.values() and row_dict[k]
                }
                address = Address.objects.get_or_create(**address_object_dict)[
                    0
                ]
                listing_object_dict["address"] = address
                Listing.objects.get_or_create(**listing_object_dict)
