from django.urls import include, path
from real_estate import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("addresses", views.AddressViewSet)
router.register("listings", views.ListingViewSet)

app_name = "real_estate"

urlpatterns = [
    path("", include(router.urls), name="listings"),
]
