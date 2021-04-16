from django.conf import settings
from django.contrib.admin.utils import unquote
from django.db.models.expressions import RawSQL
from django.template import Template
from django.utils.translation import gettext_lazy as _
from django.utils.text import format_lazy

from data_admin.boot import getAttributeFields
from .models import (
    Location,
    Customer,
    Demand,
    Item,
)
from data_admin.common.report import (
    GridReport,
    GridFieldLastModified,
    GridFieldDateTime,
    GridFieldText,
    GridFieldHierarchicalText,
    GridFieldNumber,
    GridFieldInteger,
    GridFieldCurrency,
    GridFieldChoice,
    GridFieldDuration,
)

import logging

logger = logging.getLogger(__name__)


class LocationList(GridReport):
    title = _("locations")
    basequeryset = Location.objects.all()
    model = Location
    frozenColumns = 1
    help_url = "example1/locations.html"
    message_when_empty = Template(
        """
        <h3>Define locations</h3>
        <br>
        A basic piece of master data is the list of locations where production is happening or inventory is kept.<br>
        <br><br>
        <div role="group" class="btn-group.btn-group-justified">
        <a href="{{request.prefix}}/data/example1/location/add/" class="btn btn-primary">Create a single location<br>in a form</a>
        </div>
        <br>
        """
    )

    rows = (
        GridFieldHierarchicalText(
            "name",
            title=_("name"),
            key=True,
            formatter="detail",
            extra='"role":"example1/location"',
            model=Location,
        ),
        GridFieldText("description", title=_("description")),
        GridFieldText("category", title=_("category"), initially_hidden=True),
        GridFieldText("subcategory", title=_("subcategory"), initially_hidden=True),
        GridFieldText(
            "owner",
            title=_("owner"),
            field_name="owner__name",
            formatter="detail",
            extra='"role":"example1/location"',
        ),
        GridFieldText("source", title=_("source"), initially_hidden=True),
        GridFieldLastModified("lastmodified"),
    )


class CustomerList(GridReport):
    title = _("customers")
    basequeryset = Customer.objects.all()
    model = Customer
    frozenColumns = 1
    help_url = "example1/customers.html"
    message_when_empty = Template(
        """
        <h3>Define customers</h3>
        <br>
        A basic piece of master data is the customers buying items from us.<br>
        <br><br>
        <div role="group" class="btn-group.btn-group-justified">
        <a href="{{request.prefix}}/data/example1/customer/add/" class="btn btn-primary">Create a single customer<br> in a form</a>
        </div>
        <br>
        """
    )

    rows = (
        GridFieldHierarchicalText(
            "name",
            title=_("name"),
            key=True,
            formatter="detail",
            extra='"role":"example1/customer"',
            model=Customer,
        ),
        GridFieldText("description", title=_("description")),
        GridFieldText("category", title=_("category"), initially_hidden=True),
        GridFieldText("subcategory", title=_("subcategory"), initially_hidden=True),
        GridFieldText(
            "owner",
            title=_("owner"),
            field_name="owner__name",
            formatter="detail",
            extra='"role":"example1/customer"',
        ),
        GridFieldText("source", title=_("source"), initially_hidden=True),
        GridFieldLastModified("lastmodified"),
    )


class ItemList(GridReport):
    title = _("items")
    basequeryset = Item.objects.all()
    model = Item
    frozenColumns = 1
    editable = True
    help_url = "example1/items.html"
    message_when_empty = Template(
        """
        <h3>Define items</h3>
        <br>
        A basic piece of master data is the list of items to plan.<br>
        End products, intermediate products and raw materials all need to be defined.<br>
        <br><br>
        <div role="group" class="btn-group.btn-group-justified">
        <a href="{{request.prefix}}/data/example1/item/add/" class="btn btn-primary">Create a single item<br>in a form</a>
        </div>
        <br>
        """
    )

    rows = (
        GridFieldHierarchicalText(
            "name",
            title=_("name"),
            key=True,
            formatter="detail",
            extra='"role":"example1/item"',
            model=Item,
        ),
        GridFieldText("description", title=_("description")),
        GridFieldText("category", title=_("category"), initially_hidden=True),
        GridFieldText("subcategory", title=_("subcategory"), initially_hidden=True),
        GridFieldText(
            "owner",
            title=_("owner"),
            field_name="owner__name",
            formatter="detail",
            extra='"role":"example1/item"',
        ),
        GridFieldCurrency("cost", title=_("cost")),
        GridFieldNumber("weight", title=_("weight"), initially_hidden=True),
        GridFieldNumber("volume", title=_("volume"), initially_hidden=True),
        GridFieldChoice(
            "type", title=_("type"), choices=Item.types, initially_hidden=True
        ),
        GridFieldText("source", title=_("source"), initially_hidden=True),
        GridFieldLastModified("lastmodified"),
    )


class DemandList(GridReport):
    title = _("sales orders")
    model = Demand
    frozenColumns = 1
    help_url = "example1/sales-orders.html"
    message_when_empty = Template(
        """
        <h3>Define sales orders</h3>
        <br>
        The sales orders table contains all the orders placed by your customers.<br><br>
        Orders in the status "open" are still be delivered and will be planned.<br><br>
        <br><br>
        <div role="group" class="btn-group.btn-group-justified">
        <a href="{{request.prefix}}/data/example1/demand/add/" class="btn btn-primary">Create a single sales order<br>in a form</a>
        </div>
        <br>
        """
    )

    @classmethod
    def initialize(reportclass, request):
        if reportclass._attributes_added != 2:
            reportclass._attributes_added = 2
            reportclass.attr_sql = ""
            # Adding custom item attributes
            for f in getAttributeFields(
                Item, related_name_prefix="item", initially_hidden=True
            ):
                reportclass.rows += (f,)
                reportclass.attr_sql += "item.%s, " % f.name.split("__")[-1]
            # Adding custom location attributes
            for f in getAttributeFields(
                Location, related_name_prefix="location", initially_hidden=True
            ):
                reportclass.rows += (f,)
                reportclass.attr_sql += "location.%s, " % f.name.split("__")[-1]
            # Adding custom customer attributes
            for f in getAttributeFields(
                Customer, related_name_prefix="customer", initially_hidden=True
            ):
                reportclass.rows += (f,)
                reportclass.attr_sql += "customer.%s, " % f.name.split("__")[-1]
            # Adding custom demand attributes
            for f in getAttributeFields(Demand, initially_hidden=True):
                reportclass.rows += (f,)
                reportclass.attr_sql += "demand.%s, " % f.name.split("__")[-1]

    @classmethod
    def basequeryset(reportclass, request, *args, **kwargs):

        q = Demand.objects.all()

        if "item" in request.GET:
            item = Item.objects.using(request.database).get(
                name__exact=unquote(request.GET["item"])
            )
            q = q.filter(item__lft__gte=item.lft, item__lft__lt=item.rght)
        if "location" in request.GET:
            location = Location.objects.using(request.database).get(
                name__exact=unquote(request.GET["location"])
            )
            q = q.filter(
                location__lft__gte=location.lft, location__lft__lt=location.rght
            )
        if "customer" in request.GET:
            customer = Customer.objects.using(request.database).get(
                name__exact=unquote(request.GET["customer"])
            )
            q = q.filter(customer_lft__gte=customer.lft, customer_lft__lt=customer.rght)
        if "status_in" in request.GET:
            status = unquote(request.GET["status_in"])
            q = q.filter(status__in=status.split(","))

        return q

    rows = (
        GridFieldText(
            "name",
            title=_("name"),
            key=True,
            formatter="detail",
            extra='"role":"example1/demand"',
        ),
        GridFieldHierarchicalText(
            "item",
            title=_("item"),
            field_name="item__name",
            formatter="detail",
            extra='"role":"example1/item"',
            model=Item,
        ),
        GridFieldHierarchicalText(
            "location",
            title=_("location"),
            field_name="location__name",
            formatter="detail",
            extra='"role":"example1/location"',
            model=Location,
        ),
        GridFieldHierarchicalText(
            "customer",
            title=_("customer"),
            field_name="customer__name",
            formatter="detail",
            extra='"role":"example1/customer"',
            model=Customer,
        ),
        GridFieldChoice("status", title=_("status"), choices=Demand.demandstatus),
        GridFieldNumber("quantity", title=_("quantity")),
        GridFieldDateTime("due", title=_("due")),
        GridFieldText("description", title=_("description"), initially_hidden=True),
        GridFieldText("category", title=_("category"), initially_hidden=True),
        GridFieldText("subcategory", title=_("subcategory"), initially_hidden=True),
        GridFieldText("source", title=_("source"), initially_hidden=True),
        GridFieldLastModified("lastmodified"),
        # Optional fields referencing the item
        GridFieldText(
            "item__type",
            title=format_lazy("{} - {}", _("item"), _("type")),
            initially_hidden=True,
            editable=False,
        ),
        GridFieldText(
            "item__description",
            title=format_lazy("{} - {}", _("item"), _("description")),
            initially_hidden=True,
            editable=False,
        ),
        GridFieldText(
            "item__category",
            title=format_lazy("{} - {}", _("item"), _("category")),
            initially_hidden=True,
            editable=False,
        ),
        GridFieldText(
            "item__subcategory",
            title=format_lazy("{} - {}", _("item"), _("subcategory")),
            initially_hidden=True,
            editable=False,
        ),
        GridFieldText(
            "item__owner",
            title=format_lazy("{} - {}", _("item"), _("owner")),
            field_name="item__owner__name",
            initially_hidden=True,
            editable=False,
            formatter="detail",
            extra='"role":"example1/item"',
        ),
        GridFieldCurrency(
            "item__cost",
            title=format_lazy("{} - {}", _("item"), _("cost")),
            initially_hidden=True,
            editable=False,
        ),
        GridFieldNumber(
            "item__volume",
            title=format_lazy("{} - {}", _("item"), _("volume")),
            initially_hidden=True,
            editable=False,
        ),
        GridFieldNumber(
            "item__weight",
            title=format_lazy("{} - {}", _("item"), _("weight")),
            initially_hidden=True,
            editable=False,
        ),
        GridFieldText(
            "item__source",
            title=format_lazy("{} - {}", _("item"), _("source")),
            initially_hidden=True,
            editable=False,
        ),
        GridFieldLastModified(
            "item__lastmodified",
            title=format_lazy("{} - {}", _("item"), _("last modified")),
            initially_hidden=True,
            editable=False,
        ),
        # Optional fields referencing the location
        GridFieldText(
            "location__description",
            title=format_lazy("{} - {}", _("location"), _("description")),
            initially_hidden=True,
            editable=False,
        ),
        GridFieldText(
            "location__category",
            title=format_lazy("{} - {}", _("location"), _("category")),
            initially_hidden=True,
            editable=False,
        ),
        GridFieldText(
            "location__subcategory",
            title=format_lazy("{} - {}", _("location"), _("subcategory")),
            initially_hidden=True,
            editable=False,
        ),
        GridFieldText(
            "location__owner",
            title=format_lazy("{} - {}", _("location"), _("owner")),
            initially_hidden=True,
            field_name="location__owner__name",
            formatter="detail",
            extra='"role":"example1/location"',
            editable=False,
        ),
        GridFieldText(
            "location__source",
            title=format_lazy("{} - {}", _("location"), _("source")),
            initially_hidden=True,
            editable=False,
        ),
        GridFieldLastModified(
            "location__lastmodified",
            title=format_lazy("{} - {}", _("location"), _("last modified")),
            initially_hidden=True,
            editable=False,
        ),
        # Optional fields referencing the customer
        GridFieldText(
            "customer__description",
            title=format_lazy("{} - {}", _("customer"), _("description")),
            initially_hidden=True,
            editable=False,
        ),
        GridFieldText(
            "customer__category",
            title=format_lazy("{} - {}", _("customer"), _("category")),
            initially_hidden=True,
            editable=False,
        ),
        GridFieldText(
            "customer__subcategory",
            title=format_lazy("{} - {}", _("customer"), _("subcategory")),
            initially_hidden=True,
            editable=False,
        ),
        GridFieldText(
            "customer__owner",
            title=format_lazy("{} - {}", _("customer"), _("owner")),
            initially_hidden=True,
            field_name="customer__owner__name",
            formatter="detail",
            extra='"role":"example1/customer"',
            editable=False,
        ),
        GridFieldText(
            "customer__source",
            title=format_lazy("{} - {}", _("customer"), _("source")),
            initially_hidden=True,
            editable=False,
        ),
        GridFieldLastModified(
            "customer__lastmodified",
            title=format_lazy("{} - {}", _("customer"), _("last modified")),
            initially_hidden=True,
            editable=False,
        ),
    )

    actions = [
        {
            "name": "inquiry",
            "label": format_lazy(_("change status to {status}"), status=_("inquiry")),
            "function": "grid.setStatus('inquiry')",
        },
        {
            "name": "quote",
            "label": format_lazy(_("change status to {status}"), status=_("quote")),
            "function": "grid.setStatus('quote')",
        },
        {
            "name": "open",
            "label": format_lazy(_("change status to {status}"), status=_("open")),
            "function": "grid.setStatus('open')",
        },
        {
            "name": "closed",
            "label": format_lazy(_("change status to {status}"), status=_("closed")),
            "function": "grid.setStatus('closed')",
        },
        {
            "name": "canceled",
            "label": format_lazy(_("change status to {status}"), status=_("canceled")),
            "function": "grid.setStatus('canceled')",
        },
    ]
