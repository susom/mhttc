"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

from django.views.generic.base import TemplateView
from django.urls import include, re_path
import mhttc.apps.base.views as views

urlpatterns = [
    re_path(r"^$", views.index_view, name="index"),
    re_path(r"^quick-links/?$", views.quick_links_view, name="quick_links"),
    re_path(r"^zoom-request/?$", views.zoom_request_view, name="zoom_request"),
    re_path(r"^groups/?$", views.groups_view, name="groups"),
    re_path(r"^contact/?$", views.contact_view, name="contact"),
    re_path(r"^terms/?$", views.terms_view, name="terms"),
    re_path(r"^privacy-policy/?$", views.terms_view, name="privacy-policy"),
    re_path(r"^search/?$", views.search_view, name="search"),
    re_path(r"^searching/?$", views.run_search, name="running_search"),
    re_path(r"^search/(?P<query>.+?)/?$", views.search_view, name="search_query"),
    re_path(
        r"^robots\.txt/$",
        TemplateView.as_view(
            template_name="base/robots.txt", content_type="text/plain"
        ),
    ),
]
