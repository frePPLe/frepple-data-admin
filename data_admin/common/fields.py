import json

import django.db.models as models

#
# JSONFIELD
#
# JSONField is a generic textfield that serializes/unserializes JSON objects.
#
# This code is very loosely inspired on the code found at:
#    https://github.com/bradjasper/django-jsonfield
class JSONField(models.TextField):
    def __init__(self, *args, **kwargs):
        self.dump_kwargs = kwargs.pop("dump_kwargs", {"separators": (",", ":")})
        self.load_kwargs = kwargs.pop("load_kwargs", {})
        super().__init__(*args, **kwargs)

    def to_python(self, value):
        """Convert a json string to a Python value."""
        if isinstance(value, str) and value:
            return json.loads(value)
        else:
            return value

    def get_db_prep_value(self, value, connection, prepared=False):
        """Convert JSON object to a string."""
        if self.null and value is None:
            return None
        return json.dumps(value, **self.dump_kwargs)

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_db_prep_value(value, None)

    def value_from_object(self, obj):
        value = super().value_from_object(obj)
        if self.null and value is None:
            return None
        return self.dumps_for_display(value)

    def dumps_for_display(self, value):
        return json.dumps(value)

    def db_type(self, connection):
        # A json field stores the data as a text string, that is parsed whenever
        # a json operation is performed on the field.
        return "json"


class JSONBField(JSONField):
    def db_type(self, connection):
        # A jsonb field is 1) much more efficient in querying the field,
        # 2) allows indexes to be defined on the content, but 3) takes a bit
        # more time to update.
        return "jsonb"


#
# ALIASFIELD
#


class AliasField(models.Field):
    """
    This field is an alias for another database field

    Sources:
    https://shezadkhan.com/aliasing-fields-in-django/

    Note: This uses some django functions that are being deprecated in django 2.0.
    """

    def contribute_to_class(self, cls, name, private_only=False):
        super().contribute_to_class(cls, name, private_only=True)
        setattr(cls, name, self)

    def __set__(self, instance, value):
        setattr(instance, self.db_column, value)

    def __get__(self, instance, instance_type=None):
        return getattr(instance, self.db_column)


class AliasDateTimeField(models.DateTimeField):
    """
    This field is an alias for another database field

    Sources:
    https://shezadkhan.com/aliasing-fields-in-django/

    Note: This uses some django functions that are being deprecated in django 2.0.
    """

    def contribute_to_class(self, cls, name, private_only=False):
        super().contribute_to_class(cls, name, private_only=True)
        setattr(cls, name, self)

    def __set__(self, instance, value):
        setattr(instance, self.db_column, value)

    def __get__(self, instance, instance_type=None):
        return getattr(instance, self.db_column)
