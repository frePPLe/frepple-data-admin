from django.utils.translation import gettext_lazy as _
from django.contrib import admin

from . import models
from data_admin.common.adminforms import MultiDBModelAdmin, MultiDBTabularInline

from data_admin.admin import data_site
from data_admin.boot import getAttributes


@admin.register(models.Location, site=data_site)
class Location_admin(MultiDBModelAdmin):
    model = models.Location
    raw_id_fields = ("owner",)
    save_on_top = True
    fieldsets = (
        (None, {"fields": ("name", "owner")}),
        (
            _("advanced"),
            {
                "fields": ["description", "category", "subcategory", "available"]
                + [a[0] for a in getAttributes(models.Location) if a[3]],
                "classes": ("collapse",),
            },
        ),
    )
    tabs = [
        {
            "name": "edit",
            "label": _("edit"),
            "view": "admin:example1_location_change",
            "permissions": "example1.change_location",
        },
        {
            "name": "messages",
            "label": _("messages"),
            "view": "admin:example1_location_comment",
        },
    ]


@admin.register(models.Customer, site=data_site)
class Customer_admin(MultiDBModelAdmin):
    model = models.Customer
    raw_id_fields = ("owner",)
    save_on_top = True
    fieldsets = (
        (None, {"fields": ("name", "description", "owner")}),
        (
            _("advanced"),
            {
                "fields": ["category", "subcategory"]
                + [a[0] for a in getAttributes(models.Location) if a[3]],
                "classes": ("collapse",),
            },
        ),
    )
    tabs = [
        {
            "name": "edit",
            "label": _("edit"),
            "view": "admin:example1_customer_change",
            "permissions": "example1.change_customer",
        },
        {
            "name": "messages",
            "label": _("messages"),
            "view": "admin:example1_customer_comment",
        },
    ]


@admin.register(models.Item, site=data_site)
class Item_admin(MultiDBModelAdmin):
    model = models.Item
    save_on_top = True
    raw_id_fields = ("owner",)
    search_fields = ("name", "description")
    fieldsets = (
        (None, {"fields": ("name", "description", "cost", "owner")}),
        (
            _("advanced"),
            {
                "fields": ["category", "subcategory", "type", "volume", "weight"]
                + [a[0] for a in getAttributes(models.Item) if a[3]],
                "classes": ("collapse",),
            },
        ),
    )
    tabs = [
        {
            "name": "edit",
            "label": _("edit"),
            "view": "admin:example1_item_change",
            "permissions": "example1.change_item",
        },
        {
            "name": "messages",
            "label": _("messages"),
            "view": "admin:example1_item_comment",
        },
    ]


@admin.register(models.Demand, site=data_site)
class Demand_admin(MultiDBModelAdmin):
    model = models.Demand
    raw_id_fields = ("customer", "item", "owner")
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    "item",
                    "location",
                    "customer",
                    "due",
                    "quantity",
                    "priority",
                    "status",
                )
            },
        ),
        (
            _("advanced"),
            {
                "fields": [
                    "description",
                    "category",
                    "subcategory",
                ]
                + [a[0] for a in getAttributes(models.Demand) if a[3]],
                "classes": ("collapse",),
            },
        ),
    )
    save_on_top = True
    tabs = [
        {
            "name": "edit",
            "label": _("edit"),
            "view": "admin:example1_demand_change",
            "permissions": "example1.change_demand",
        },
        {
            "name": "messages",
            "label": _("messages"),
            "view": "admin:example1_demand_comment",
        },
    ]
