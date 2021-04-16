from importlib import import_module

from django.conf import settings
from django.contrib.admin.sites import AdminSite, AlreadyRegistered
from django.contrib.admin.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _


class freppleAuthenticationForm(AuthenticationForm):
    error_messages = {
        "invalid_login": _(
            "Please enter a correct %(username)s and password. Note that both fields may be case-sensitive."
        ),
        "inactive": _("This user is inactive."),
    }


class freppleAdminSite(AdminSite):

    login_form = freppleAuthenticationForm

    def register(self, model_or_iterable, admin_class=None, force=False, **options):
        try:
            super().register(model_or_iterable, admin_class, **options)
        except AlreadyRegistered:
            # Ignore exception if the model is already registered. It indicates that
            # another app has already registered it.
            if force:
                # Unregister the previous one and register ourselves
                self.unregister(model_or_iterable)
                super().register(model_or_iterable, admin_class, **options)


# Create two admin sites where all our apps will register their models
data_site = freppleAdminSite(name="data")

# Adding the admin modules of each installed application.
for app in settings.INSTALLED_APPS:
    try:
        mod = import_module("%s.admin" % app)
    except ImportError as e:
        # Silently ignore if its the admin module which isn't found
        if str(e) not in (
            "No module named %s.admin" % app,
            "No module named '%s.admin'" % app,
        ):
            raise e
