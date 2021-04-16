"""
The boot app is placed at the top of the list in ``INSTALLED_APPS``
for the purpose of hooking into Django's ``class_prepared`` signal
and defining attribute fields.

This app is very closely inspired on http://mezzanine.jupo.org/
and its handling of injected extra fields.
"""
from importlib import import_module

from django.conf import settings
from django.db import models

from django.core.exceptions import ImproperlyConfigured
from django.db.models.signals import class_prepared

from ..common.fields import JSONBField


_register = {}
_register_kwargs = {}


def add_extra_model_fields(sender, **kwargs):
    model_path = "%s.%s" % (sender.__module__, sender.__name__)
    for field_name, label, fieldtype, editable, initially_hidden in _register.get(
        model_path, []
    ):

        register_args = (
            _register_kwargs[(model_path, field_name)]
            if (model_path, field_name) in _register_kwargs
            else None
        )

        if fieldtype == "string":
            if register_args and "max_length" in register_args:
                max_length = register_args["max_length"]
            else:
                max_length = 300
            field = models.CharField(
                label,
                max_length=max_length,
                null=True,
                blank=True,
                db_index=True,
                editable=editable,
            )
        elif fieldtype == "boolean":
            field = models.NullBooleanField(
                label, null=True, blank=True, db_index=True, editable=editable
            )
        elif fieldtype == "number":
            # Note: Other numeric fields have precision 20, 8.
            # Changing the value below would require migrating existing attributes of all projects.
            if register_args:
                max_digits = register_args.get("max_digits", 15)
                decimal_places = register_args.get("decimal_places", 6)
            else:
                max_digits = 15
                decimal_places = 6
            field = models.DecimalField(
                label,
                max_digits=max_digits,
                decimal_places=decimal_places,
                null=True,
                blank=True,
                db_index=True,
                editable=editable,
            )
        elif fieldtype == "integer":
            field = models.IntegerField(
                label, null=True, blank=True, db_index=True, editable=editable
            )
        elif fieldtype == "date":
            field = models.DateField(
                label, null=True, blank=True, db_index=True, editable=editable
            )
        elif fieldtype == "datetime":
            field = models.DateTimeField(
                label, null=True, blank=True, db_index=True, editable=editable
            )
        elif fieldtype == "duration":
            field = models.DurationField(
                label, null=True, blank=True, db_index=True, editable=editable
            )
        elif fieldtype == "time":
            field = models.TimeField(
                label, null=True, blank=True, db_index=True, editable=editable
            )
        elif fieldtype == "jsonb":
            field = JSONBField(default="{}", null=True, blank=True, editable=editable)
        else:
            raise ImproperlyConfigured("Invalid attribute type '%s'." % fieldtype)
        field.contribute_to_class(sender, field_name)


def registerAttribute(model, attrlist, **kwargs):
    """
    Register a new attribute.
    The attribute list is passed as a list of tuples in the format
      fieldname, label, fieldtype, editable (default=True), initially_hidden (default=False)
    """
    if model not in _register:
        _register[model] = []
    for attr in attrlist:
        if len(attr) < 3:
            raise Exception("Invalid attribute definition: %s" % attr)
        elif len(attr) == 3:
            _register[model].append(attr + (True, False))
        elif len(attr) == 4:
            _register[model].append(attr + (False,))
        else:
            _register[model].append(attr)

        if kwargs:
            _register_kwargs[(model, attr[0])] = kwargs


def getAttributes(model):
    """
    Return all attributes for a given model in the format:
      fieldname, label, fieldtype, editable (default=True), initially_hidden (default=False)
    """
    for attr in _register.get("%s.%s" % (model.__module__, model.__name__), []):
        yield attr
    for base in model.__bases__:
        if hasattr(base, "_meta"):
            for attr in getAttributes(base):
                yield attr


def getAttributeFields(model, related_name_prefix=None, initially_hidden=False):
    """
    Return report fields for all attributes of a given model.
    """
    from ..common.report import GridFieldText, GridFieldBool, GridFieldNumber
    from ..common.report import (
        GridFieldInteger,
        GridFieldDate,
        GridFieldDateTime,
    )
    from ..common.report import GridFieldDuration, GridFieldTime

    result = []
    for field_name, label, fieldtype, editable, hidden in getAttributes(model):
        if related_name_prefix:
            field_name = "%s__%s" % (related_name_prefix, field_name)
            label = "%s - %s" % (related_name_prefix.split("__")[-1], label)
        else:
            label = "%s - %s" % (model.__name__, label)
        if fieldtype == "string":
            result.append(
                GridFieldText(
                    field_name,
                    title=label,
                    initially_hidden=hidden or initially_hidden,
                    editable=editable,
                )
            )
        elif fieldtype == "boolean":
            result.append(
                GridFieldBool(
                    field_name,
                    title=label,
                    initially_hidden=hidden or initially_hidden,
                    editable=editable,
                )
            )
        elif fieldtype == "number":
            result.append(
                GridFieldNumber(
                    field_name,
                    title=label,
                    initially_hidden=hidden or initially_hidden,
                    editable=editable,
                )
            )
        elif fieldtype == "integer":
            result.append(
                GridFieldInteger(
                    field_name,
                    title=label,
                    initially_hidden=hidden or initially_hidden,
                    editable=editable,
                )
            )
        elif fieldtype == "date":
            result.append(
                GridFieldDate(
                    field_name,
                    title=label,
                    initially_hidden=hidden or initially_hidden,
                    editable=editable,
                )
            )
        elif fieldtype == "datetime":
            result.append(
                GridFieldDateTime(
                    field_name,
                    title=label,
                    initially_hidden=hidden or initially_hidden,
                    editable=editable,
                )
            )
        elif fieldtype == "duration":
            result.append(
                GridFieldDuration(
                    field_name,
                    title=label,
                    initially_hidden=hidden or initially_hidden,
                    editable=editable,
                )
            )
        elif fieldtype == "time":
            result.append(
                GridFieldTime(
                    field_name,
                    title=label,
                    initially_hidden=hidden or initially_hidden,
                    editable=editable,
                )
            )
        elif fieldtype == "jsonb":
            result.append(
                GridFieldText(
                    field_name,
                    title=label,
                    initially_hidden=hidden or initially_hidden,
                    editable=editable,
                )
            )
        else:
            raise Exception("Invalid attribute type '%s'." % fieldtype)
    return result


_first = True
if _first:
    _first = False
    # Scan attribute definitions from the settings
    for model, attrlist in settings.ATTRIBUTES:
        registerAttribute(model, attrlist)

    # Scan attribute definitions from the installed apps
    for app in reversed(settings.INSTALLED_APPS):
        try:
            mod = import_module("%s.attributes" % app)
        except ImportError as e:
            # Silently ignore if it's the menu module which isn't found
            if str(e) not in (
                "No module named %s.attributes" % app,
                "No module named '%s.attributes'" % app,
            ):
                raise e

    if _register:
        class_prepared.connect(
            add_extra_model_fields, dispatch_uid="frepple_attribute_injection"
        )
