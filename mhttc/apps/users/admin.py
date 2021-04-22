"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

from django.contrib import admin
from mhttc.apps.users.models import User, Center, CenterGroup


class CenterAdmin(admin.ModelAdmin):
    fields = (
        "name",
        "email",
        "owners",
        "full_access",
        "center_group",
    )

class CenterGroupAdmin(admin.ModelAdmin):
    fields = (
        "name",
    )

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        if not obj.pk:
            obj.created_by = request.user
        else:
            obj.updated_by = request.user
        super().save_model(request, obj, form, change)

admin.site.register(User)
admin.site.register(Center, CenterAdmin)
admin.site.register(CenterGroup, CenterGroupAdmin)
