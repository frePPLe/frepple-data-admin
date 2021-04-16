from data_admin.menu import menu

from . import views
from . import models

menu.addGroup("example1", label="example1", index=100)
menu.addItem(
    "example1",
    "demand",
    url="/data/example1/demand/",
    report=views.DemandList,
    index=100,
    model=models.Demand,
    dependencies=[models.Item, models.Location, models.Customer],
)
menu.addItem(
    "example1",
    "item",
    url="/data/example1/item/",
    report=views.ItemList,
    index=1100,
    model=models.Item,
)
menu.addItem(
    "example1",
    "locations",
    url="/data/example1/location/",
    report=views.LocationList,
    index=1150,
    model=models.Location,
)
menu.addItem(
    "example1",
    "customer",
    url="/data/example1/customer/",
    report=views.CustomerList,
    index=1200,
    model=models.Customer,
)
