"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

from django.urls import path
from mhttc.apps.main import views


urlpatterns = [
    # Projects
    path("projects/", views.all_projects, name="all_projects"),
    path("u/projects/", views.user_projects, name="user_projects"),
    path("projects/new/", views.new_project, name="new_project"),
    path("projects/<uuid:uuid>/delete", views.delete_project, name="delete_project"),
    path("projects/search/", views.search_project, name="search_project"),
    path("project/<uuid:uuid>/", views.project_details, name="project_details"),
    path(
        "project/forms/<uuid:uuid>/<int:stage>/edit",
        views.edit_form_template,
        name="edit_form_template",
    ),
    path(
        "project/forms/<uuid:uuid>/", views.view_project_form, name="view_project_form"
    ),
    path(
        "project/forms/<uuid:uuid>/generate/", views.generate_form_pdf, name="generate_project_form"
    ),
    path(
        "project/forms/download/<str:file_name>/", views.download_form_pdf, name="download_project_form"
    ),
    path(
        "project/<uuid:uuid>/publish", views.publish_project, name="publish_project"
    ),
    # Events
    path("event/new/", views.new_event, name="new_event"),
    path(
        "event/<uuid:uuid>/certificate/",
        views.download_certificate,
        name="download_certificate",
    ),
    path(
        "event/<uuid:uuid>/update/image",
        views.update_event_image,
        name="update_event_image",
    ),
    path("event/<uuid:uuid>/edit", views.edit_event, name="edit_event"),
    path("event/<uuid:uuid>/delete", views.delete_event, name="delete_event"),
    path("event/<uuid:uuid>/", views.event_details, name="event_details"),
    path("center/events/", views.center_events, name="center_events"),
]
