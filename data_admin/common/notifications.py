from .models import NotificationFactory, User


@NotificationFactory.register(User, [User])
def UserNotification(flw, msg):
    return flw.content_type == msg.content_type and flw.object_pk == msg.object_pk
