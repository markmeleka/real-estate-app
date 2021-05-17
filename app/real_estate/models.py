from django.db import models


class Address(models.Model):
    street_address = models.CharField(max_length=255)
    unit_number = models.CharField(max_length=16, null=True)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zipcode = models.CharField(max_length=16)
    country = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=11, decimal_places=8, null=True)
    longitude = models.DecimalField(max_digits=11, decimal_places=8, null=True)

    def __str__(self):
        _unit_num = f"{self.unit_number}-" if self.unit_number else ""
        return f"{_unit_num}{self.street_address}, {self.city}, {self.state}"


class Listing(models.Model):
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    listing_number = models.CharField(max_length=255)
    date_accessed = models.DateField()
    price = models.IntegerField()
    details_url = models.CharField(max_length=255)
    size_interior = models.CharField(max_length=255, null=True)
    bedrooms = models.CharField(max_length=8)  # "1 + 1"
    # num_bathrooms example: 1.5 bathrooms
    num_bathrooms = models.DecimalField(max_digits=4, decimal_places=2)
    num_stories = models.DecimalField(
        max_digits=6, decimal_places=2, null=True
    )
    num_units = models.IntegerField(null=True)
    land_size = models.CharField(max_length=255, null=True)
    frontage = models.CharField(max_length=255, null=True)
    photo_link = models.CharField(max_length=255, null=True)
    property_type = models.CharField(max_length=255)
    building_type = models.CharField(max_length=255)
    ownership_type = models.CharField(max_length=255)
    parking_type = models.CharField(max_length=255, null=True)
    num_parking = models.IntegerField(null=True)
    description = models.TextField(null=True)

    def __str__(self):
        return f"{self.listing_number}: {self.address}"
