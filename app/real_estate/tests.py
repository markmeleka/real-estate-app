from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from real_estate.models import Address, Listing
from real_estate.serializers import (
    AddressListSerializer,
    AddressSerializer,
    ListingListSerializer,
    ListingSerializer,
)
from rest_framework import status
from rest_framework.test import APIClient

ADDRESSES_URL = reverse("real_estate:address-list")
LISTINGS_URL = reverse("real_estate:listing-list")


def get_address_detail_url(address_id):
    return reverse("real_estate:address-detail", args=[address_id])


def get_listing_detail_url(listing_id):
    return reverse("real_estate:listing-detail", args=[listing_id])


def get_sample_address_payload(**params):
    address_payload = {
        "street_address": "100 Regina St. S.",
        "unit_number": "1",
        "city": "Waterloo",
        "state": "Ontario",
        "country": "Canada",
        "zipcode": "N2J4P9",
        "longitude": -80.52039787,
        "latitude": 43.46340842,
    }
    address_payload.update(params)

    return address_payload


def get_sample_listing_payload(**params):
    address_payload = get_sample_address_payload()

    listing_payload = {
        "address": address_payload,
        "listing_number": 99995555,
        "date_accessed": "2021-05-16",
        "price": 1000000,
        "description": "Move to Waterloo today!",
        "details_url": "realtor.ca/real-estate/",
        "size_interior": 1050.00,
        "bedrooms": "3 + 1",
        "num_bathrooms": "1.5",
        "num_stories": 2,
        "num_units": 0,
        "photo_link": (
            "https://www.waterloo.ca/en/images/structure/logo_black.svg"
        ),
        "land_size": "under 1/2 acre",
        "frontage": "80 ft",
        "property_type": "Single Family",
        "building_type": "House",
        "ownership_type": "Freehold",
        "parking_type": "covered",
        "num_parking": 4,
    }
    listing_payload.update(params)
    return listing_payload


def create_sample_address(**params):
    address = get_sample_address_payload(**params)
    return Address.objects.create(**address)


def create_sample_listing(**params):
    if "address" not in params:
        address = create_sample_address()
        params["address"] = address
    listing = get_sample_listing_payload(**params)
    return Listing.objects.create(**listing)


class PublicRealEstateApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(LISTINGS_URL)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class PrivateRealEstateApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_address_detail(self):
        address = create_sample_address()
        address_detail_url = get_address_detail_url(address.id)
        response = self.client.get(address_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        serializer = AddressSerializer(address)
        self.assertEqual(response.data, serializer.data)

    def test_retrieve_addresses(self):
        create_sample_address()
        create_sample_address()
        response = self.client.get(ADDRESSES_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_results = response.data["results"]
        addresses = Address.objects.all().order_by("id")
        serializer = AddressListSerializer(addresses, many=True)
        self.assertEqual(len(response_results), 2)
        self.assertEqual(response_results, serializer.data)

    def test_retrieve_listing_detail(self):
        listing = create_sample_listing()
        listing_detail_url = get_listing_detail_url(listing.id)
        response = self.client.get(listing_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        serializer = ListingSerializer(listing)
        self.assertEqual(response.data, serializer.data)

    def test_retrieve_listings(self):
        create_sample_listing()
        create_sample_listing()
        response = self.client.get(LISTINGS_URL)
        response_results = response.data["results"]
        self.assertEqual(len(response_results), 2)

        listings = Listing.objects.all().order_by("id")
        serializer = ListingListSerializer(listings, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_results, serializer.data)

    def test_create_listing(self):
        listing_payload = get_sample_listing_payload()

        response = self.client.post(
            LISTINGS_URL, listing_payload, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        listings = Listing.objects.all()
        serializer = ListingSerializer(listings, many=True)
        self.assertEqual(len(serializer.data), 1)
        self.assertEqual(response.data, serializer.data[0])

    def test_filter_listings_by_city(self):
        address = create_sample_address(city="Waterloo")
        address_to_filter = create_sample_address(city="Cambridge")
        listing = create_sample_listing(address=address)
        listing_to_filter = create_sample_listing(address=address_to_filter)
        response_all = self.client.get(LISTINGS_URL)
        self.assertEqual(response_all.status_code, status.HTTP_200_OK)

        response_all_results = response_all.data["results"]
        self.assertEqual(len(response_all_results), 2)

        response_filtered = self.client.get(
            LISTINGS_URL, {"city": "cambridge"}
        )
        self.assertEqual(response_filtered.status_code, status.HTTP_200_OK)
        response_filtered_results = response_filtered.data["results"]

        serializer = ListingListSerializer(listing)
        serializer_to_filter = ListingListSerializer(listing_to_filter)
        self.assertIn(serializer_to_filter.data, response_filtered_results)
        self.assertNotIn(serializer.data, response_filtered_results)

    def test_ordering_by_price(self):
        listing_lower_price = create_sample_listing(price=500000)
        listing_higher_price = create_sample_listing(price=600000)

        # Test ascending
        response_order_asc = self.client.get(
            LISTINGS_URL, {"ordering": "price"}
        )
        self.assertEqual(response_order_asc.status_code, status.HTTP_200_OK)
        response_order_asc_results = response_order_asc.data["results"]
        self.assertEqual(len(response_order_asc_results), 2)

        serializer_lower_price = ListingListSerializer(listing_lower_price)
        serializer_higher_price = ListingListSerializer(listing_higher_price)

        self.assertEqual(
            serializer_lower_price.data, response_order_asc_results[0]
        )
        self.assertEqual(
            serializer_higher_price.data, response_order_asc_results[1]
        )

        # Test descending
        response_order_desc = self.client.get(
            LISTINGS_URL, {"ordering": "-price"}
        )
        self.assertEqual(response_order_desc.status_code, status.HTTP_200_OK)
        response_order_desc_results = response_order_desc.data["results"]
        self.assertEqual(len(response_order_desc_results), 2)
        self.assertEqual(
            serializer_higher_price.data, response_order_desc_results[0]
        )
        self.assertEqual(
            serializer_lower_price.data, response_order_desc_results[1]
        )
