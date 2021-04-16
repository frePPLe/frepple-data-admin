from django.utils.translation import gettext_lazy as _

from ..menu import menu
from .views import TaskReport

menu.addItem(
    "admin",
    "execute",
    url="/execute/",
    label=_("Execute"),
    report=TaskReport,
    index=100,
)
