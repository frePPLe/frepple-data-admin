from data_admin.common.models import NotificationFactory
from .models import (
    Location,
    Customer,
    Item,
    Demand,
)


@NotificationFactory.register(Location, [Location, Demand])
def LocationNotification(flw, msg):
    if flw.content_type == msg.content_type:
        return flw.object_pk == msg.object_pk
    elif msg.content_type.model_class() in (Demand,):
        if flw.object_pk != msg.content_object.location_id:
            return False
        else:
            args = flw.args.get("sub", None) if flw.args else None
            return msg.model_name() in args if args else True


@NotificationFactory.register(Customer, [Customer, Demand])
def CustomerNotification(flw, msg):
    if flw.content_type == msg.content_type:
        return flw.object_pk == msg.object_pk
    elif flw.object_pk != msg.content_object.customer_id:
        return False
    else:
        args = flw.args.get("sub", None) if flw.args else None
        return msg.model_name() in args if args else True


@NotificationFactory.register(
    Item,
    [
        Item,
        Demand,
    ],
)
def ItemNotification(flw, msg):
    if flw.content_type == msg.content_type:
        return flw.object_pk == msg.object_pk
    elif msg.content_type.model_class() == Item:
        return False
    elif flw.object_pk != msg.content_object.item_id:
        return False
    else:
        args = flw.args.get("sub", None) if flw.args else None
        return msg.model_name() in args if args else True


@NotificationFactory.register(Demand, [Demand])
def DemandNotification(flw, msg):
    return flw.content_type == msg.content_type and flw.object_pk == msg.object_pk
