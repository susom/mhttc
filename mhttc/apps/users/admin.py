"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

from django.contrib import admin
from mhttc.apps.users.models import User, Center


class CenterAdmin(admin.ModelAdmin):
    fields = (
        "name",
        "email",
        "owners",
        "full_access",
    )

admin.site.register(User)
admin.site.register(Center, CenterAdmin)
