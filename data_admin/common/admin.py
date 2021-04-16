from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _

from .models import User, Comment, Follower
from .adminforms import MultiDBUserCreationForm, MultiDBModelAdmin
from ..admin import data_site


@admin.register(User, site=data_site)
class MyUserAdmin(UserAdmin, MultiDBModelAdmin):
    save_on_top = True

    add_form = MultiDBUserCreationForm
    add_fieldsets = (
        (
            _("Personal info"),
            {"fields": ("username", ("first_name", "last_name"), "email")},
        ),
        (_("password"), {"fields": ("password1", "password2")}),
        (_("scenario access"), {"fields": ("scenarios",)}),
    )

    change_user_password_template = "auth/change_password.html"
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            _("Personal info"),
            {"fields": ("first_name", "last_name", "email", "avatar")},
        ),
        (
            _("Permissions in this scenario"),
            {"fields": ("is_active", "is_superuser", "groups", "user_permissions")},
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )

    tabs = [
        {
            "name": "edit",
            "label": _("edit"),
            "view": "admin:common_user_change",
            "permission": "common.change_user",
        },
        {
            "name": "messages",
            "label": _("messages"),
            "view": "admin:common_user_comment",
        },
    ]

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ("last_login", "date_joined")
        return self.readonly_fields

    def has_delete_permission(self, request, obj=None):
        # Users can't be deleted. Just mark them as inactive instead
        return False


@admin.register(Group, site=data_site)
class MyGroupAdmin(MultiDBModelAdmin):
    # This class re-implements the GroupAdmin class from
    # django.contrib.auth.admin, but without the performance optimization
    # trick it uses. Our version of the Admin is slower (as it generates much
    # more database queries), but it works on frepple's multi-database setups.
    search_fields = ("name",)
    ordering = ("name",)
    filter_horizontal = ("permissions",)
    save_on_top = True
    tabs = [
        {
            "name": "edit",
            "label": _("edit"),
            "view": "admin:auth_group_change",
            "permission": "auth.change_group",
        },
        {
            "name": "messages",
            "label": _("messages"),
            "view": "admin:auth_group_comment",
        },
    ]


@admin.register(Comment, site=data_site)
class Comment_admin(MultiDBModelAdmin):
    model = Comment
    save_on_top = True


@admin.register(Follower, site=data_site)
class Follower_admin(MultiDBModelAdmin):
    model = Follower
    exclude = ("user", "args")
    save_on_top = True
