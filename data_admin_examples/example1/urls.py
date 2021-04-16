from django.conf.urls import url

from . import views
from . import serializers

# Automatically add these URLs when the application is installed
autodiscover = True

urlpatterns = [
    # Grid views
    url(
        r"^data/example1/location/$",
        views.LocationList.as_view(),
        name="example1_location_changelist",
    ),
    url(
        r"^data/example1/customer/$",
        views.CustomerList.as_view(),
        name="example1_customer_changelist",
    ),
    url(
        r"^data/example1/demand/$",
        views.DemandList.as_view(),
        name="example1_demand_changelist",
    ),
    url(
        r"^data/example1/item/$",
        views.ItemList.as_view(),
        name="example1_item_changelist",
    ),
    # REST API framework
    url(r"^api/example1/location/$", serializers.LocationAPI.as_view()),
    url(r"^api/example1/customer/$", serializers.CustomerAPI.as_view()),
    url(r"^api/example1/demand/$", serializers.DemandAPI.as_view()),
    url(r"^api/example1/item/$", serializers.ItemAPI.as_view()),
    url(r"^api/example1/location/(?P<pk>(.+))/$", serializers.LocationdetailAPI.as_view()),
    url(r"^api/example1/customer/(?P<pk>(.+))/$", serializers.CustomerdetailAPI.as_view()),
    url(r"^api/example1/demand/(?P<pk>(.+))/$", serializers.DemanddetailAPI.as_view()),
    url(r"^api/example1/item/(?P<pk>(.+))/$", serializers.ItemdetailAPI.as_view()),   
]
