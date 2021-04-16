from django.conf import settings
from django.utils.translation import gettext_lazy as _

from . import views
from . import models
from ..menu import menu


# Settings menu
menu.addItem(
    "admin",
    "parameter admin",
    url="/data/common/parameter/",
    report=views.ParameterList,
    index=1100,
    model=models.Parameter,
    admin=True,
)
menu.addItem(
    "admin",
    "bucket admin",
    url="/data/common/bucket/",
    report=views.BucketList,
    index=1200,
    model=models.Bucket,
    admin=True,
)
menu.addItem(
    "admin",
    "bucketdetail admin",
    url="/data/common/bucketdetail/",
    report=views.BucketDetailList,
    index=1300,
    model=models.BucketDetail,
    admin=True,
)
menu.addItem(
    "admin",
    "comment admin",
    url="/data/common/comment/",
    report=views.CommentList,
    index=1400,
    model=models.Comment,
    admin=True,
)

# User maintenance
menu.addItem("admin", "users", separator=True, index=2000)
menu.addItem(
    "admin",
    "user admin",
    url="/data/common/user/",
    report=views.UserList,
    index=2100,
    model=models.User,
    admin=True,
)
menu.addItem(
    "admin",
    "group admin",
    url="/data/auth/group/",
    report=views.GroupList,
    index=2200,
    permission="auth.change_group",
    admin=True,
)

# Help menu
menu.addItem(
    "help",
    "documentation",
    url=settings.DOCUMENTATION_URL,
    label=_("Documentation"),
    window=True,
    prefix=False,
    index=300,
)
menu.addItem(
    "help",
    "API",
    url="/api/",
    label=_("REST API help"),
    window=True,
    prefix=True,
    index=400,
)
