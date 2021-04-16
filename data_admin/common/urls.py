from django.conf.urls import url
from django.views.generic.base import RedirectView

from . import views
from . import serializers
from . import dashboard

from .api.views import APIIndexView
from .registration.views import (
    ResetPasswordRequestView,
    PasswordResetConfirmView,
)


# Automatically add these URLs when the application is installed
autodiscover = True

urlpatterns = [
    url(r"^uploads/(.+)$", views.uploads, name="uploads"),
    url(r"^inbox/$", views.inbox, name="inbox"),
    url(r"^follow/$", views.follow, name="follow"),
    url(r"^$", views.cockpit, name="cockpit"),
    url(r"^preferences/$", views.preferences, name="preferences"),
    url(r"^horizon/$", views.horizon, name="horizon"),
    url(r"^settings/$", views.saveSettings),
    url(
        r"^widget/(.+)/",
        dashboard.Dashboard.dispatch,
        name="dashboard",
    ),
    # Model list reports, which override standard admin screens
    url(r"^data/login/$", views.login),
    url(
        r"^data/auth/group/$",
        views.GroupList.as_view(),
        name="auth_group_changelist",
    ),
    url(
        r"^data/common/user/$",
        views.UserList.as_view(),
        name="common_user_changelist",
    ),
    url(
        r"^data/common/follower/$",
        views.FollowerList.as_view(),
        name="common_follower_changelist",
    ),
    url(
        r"^data/common/bucket/$",
        views.BucketList.as_view(),
        name="common_bucket_changelist",
    ),
    url(
        r"^data/common/bucketdetail/$",
        views.BucketDetailList.as_view(),
        name="common_bucketdetail_changelist",
    ),
    url(
        r"^data/common/parameter/$",
        views.ParameterList.as_view(),
        name="common_parameter_changelist",
    ),
    url(
        r"^data/common/comment/$",
        views.CommentList.as_view(),
        name="common_comment_changelist",
    ),
    # Special case of the next line for user password changes in the user edit screen
    url(
        r"detail/common/user/(?P<id>.+)/password/$",
        RedirectView.as_view(url="/data/common/user/%(id)s/password/"),
    ),
    # Detail URL for an object, which internally redirects to the view for the last opened tab
    url(r"^detail/([^/]+)/([^/]+)/(.+)/$", views.detail),
    # REST API framework
    url(r"^api/common/bucket/$", serializers.BucketAPI.as_view()),
    url(
        r"^api/common/bucketdetail/$",
        serializers.BucketDetailAPI.as_view(),
    ),
    url(
        r"^api/common/bucketdetail/$",
        serializers.BucketDetailAPI.as_view(),
    ),
    url(r"^api/common/parameter/$", serializers.ParameterAPI.as_view()),
    url(r"^api/common/comment/$", serializers.CommentAPI.as_view()),
    url(
        r"^api/common/bucket/(?P<pk>(.+))/$",
        serializers.BucketdetailAPI.as_view(),
    ),
    url(
        r"^api/common/bucketdetail/(?P<pk>(.+))/$",
        serializers.BucketDetaildetailAPI.as_view(),
    ),
    url(
        r"^api/common/parameter/(?P<pk>(.+))/$",
        serializers.ParameterdetailAPI.as_view(),
    ),
    url(
        r"^api/common/comment/(?P<pk>(.+))/$",
        serializers.CommentdetailAPI.as_view(),
    ),
    url(r"^api/$", APIIndexView),
    url(r"^about/$", views.AboutView, name="about"),
    # Forgotten password
    url(
        r"^reset_password_confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$",
        PasswordResetConfirmView.as_view(),
        name="reset_password_confirm",
    ),
    url(
        r"^reset_password/$", ResetPasswordRequestView.as_view(), name="reset_password"
    ),
]
