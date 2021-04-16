from django.db import models
from django.utils.translation import gettext_lazy as _

from data_admin.common.models import (
    HierarchyModel,
    AuditModel,
)


class Location(AuditModel, HierarchyModel):
    # Database fields
    description = models.CharField(
        _("description"), max_length=500, null=True, blank=True
    )
    category = models.CharField(
        _("category"), max_length=300, null=True, blank=True, db_index=True
    )
    subcategory = models.CharField(
        _("subcategory"), max_length=300, null=True, blank=True, db_index=True
    )

    def __str__(self):
        return self.name

    class Meta(AuditModel.Meta):
        db_table = "location"
        verbose_name = _("location")
        verbose_name_plural = _("locations")
        ordering = ["name"]


class Customer(AuditModel, HierarchyModel):
    # Database fields
    description = models.CharField(
        _("description"), max_length=500, null=True, blank=True
    )
    category = models.CharField(
        _("category"), max_length=300, null=True, blank=True, db_index=True
    )
    subcategory = models.CharField(
        _("subcategory"), max_length=300, null=True, blank=True, db_index=True
    )

    def __str__(self):
        return self.name

    class Meta(AuditModel.Meta):
        db_table = "customer"
        verbose_name = _("customer")
        verbose_name_plural = _("customers")
        ordering = ["name"]


class Item(AuditModel, HierarchyModel):
    types = (
        ("make to stock", _("make to stock")),
        ("make to order", _("make to order")),
    )

    # Database fields
    description = models.CharField(
        _("description"), max_length=500, null=True, blank=True
    )
    category = models.CharField(
        _("category"), max_length=300, null=True, blank=True, db_index=True
    )
    subcategory = models.CharField(
        _("subcategory"), max_length=300, null=True, blank=True, db_index=True
    )
    cost = models.DecimalField(
        _("cost"),
        null=True,
        blank=True,
        max_digits=20,
        decimal_places=8,
        help_text=_("Cost of the item"),
    )
    type = models.CharField(
        _("type"), max_length=20, null=True, blank=True, choices=types
    )
    weight = models.DecimalField(
        _("weight"),
        null=True,
        blank=True,
        max_digits=20,
        decimal_places=8,
        help_text=_("Weight of the item"),
    )
    volume = models.DecimalField(
        _("volume"),
        null=True,
        blank=True,
        max_digits=20,
        decimal_places=8,
        help_text=_("Volume of the item"),
    )

    def __str__(self):
        return self.name

    class Meta(AuditModel.Meta):
        db_table = "item"
        verbose_name = _("item")
        verbose_name_plural = _("items")
        ordering = ["name"]


class Demand(AuditModel, HierarchyModel):
    # Status
    demandstatus = (
        ("inquiry", _("inquiry")),
        ("quote", _("quote")),
        ("open", _("open")),
        ("closed", _("closed")),
        ("canceled", _("canceled")),
    )

    # Database fields
    description = models.CharField(
        _("description"), max_length=500, null=True, blank=True
    )
    category = models.CharField(
        _("category"), max_length=300, null=True, blank=True, db_index=True
    )
    subcategory = models.CharField(
        _("subcategory"), max_length=300, null=True, blank=True, db_index=True
    )
    customer = models.ForeignKey(
        Customer, verbose_name=_("customer"), db_index=True, on_delete=models.CASCADE
    )
    item = models.ForeignKey(
        Item, verbose_name=_("item"), db_index=True, on_delete=models.CASCADE
    )
    location = models.ForeignKey(
        Location, verbose_name=_("location"), db_index=True, on_delete=models.CASCADE
    )
    due = models.DateTimeField(
        _("due"), help_text=_("Due date of the sales order"), db_index=True
    )
    status = models.CharField(
        _("status"),
        max_length=10,
        null=True,
        blank=True,
        choices=demandstatus,
        default="open",
        help_text=_('Status of the demand. Only "open" demands are planned'),
    )
    quantity = models.DecimalField(
        _("quantity"), max_digits=20, decimal_places=8, default=1
    )

    # Convenience methods
    def __str__(self):
        return self.name

    class Meta(AuditModel.Meta):
        db_table = "demand"
        verbose_name = _("sales order")
        verbose_name_plural = _("sales orders")
        ordering = ["name"]
