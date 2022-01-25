"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

from django.urls import path
from django.urls import include, re_path
import mhttc.apps.users.views as views

urlpatterns = [
    # Twitter, and social auth
    re_path(r"^login/$", views.login, name="login"),
    re_path(r"^accounts/login/$", views.login),
    re_path(r"^logout/$", views.logout, name="logout"),
    re_path(r"^password/$", views.change_password, name="change_password"),
    re_path(r"^terms/agree", views.agree_terms, name="agree_terms"),
    re_path(r"^u/delete$", views.delete_account, name="delete_account"),  # delete account
    re_path(r"^u/profile", views.view_profile, name="profile"),
    re_path("^", include("django.contrib.auth.urls")),
    # Centers
    path("center/<int:uuid>/", views.center_details, name="center_details"),
    path("centers/", views.all_centers, name="all_centers"),
    path("u/center/", views.user_center, name="user_center"),
    # Users
    path("u/invite/", views.invite_users, name="invite_users"),
    path("u/invite/<uuid:uuid>", views.invited_user, name="invited_user"),
    # We don't currently have a reason for one user to see another user's account
    # url(r'^(?P<username>[A-Za-z0-9@/./+/-/_]+)/$',views.view_profile,name="profile"),
]
