"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
from django.db.models import Q
from django.contrib import admin
from mhttc.apps.main.models import Project, FormTemplate, Training, TrainingParticipant, StrategyType, Strategy
from import_export import fields, resources
from import_export.widgets import ForeignKeyWidget
from import_export.admin import ExportActionMixin


class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "status",
        "center",
        "description",
        "form",
        "contact",
    )

    fields = (
        "name",
        "description",
        "stage",
        "form",
        "center",
        "contact",
    )


class TrainingAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
        "center",
        "contact",
    )


class TrainingParticipantAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "email",
        "training",
    )

class StrategyAdmin(admin.ModelAdmin):
    fields = [
        'strategy_type',
        'strategy_format',
        'frequency',
        'planned_number_units',
    ]

    list_display = [
        'strategy_type',
        'strategy_format',
        'frequency',
        'planned_number_units',
    ]

class StrategyTypeAdmin(admin.ModelAdmin):
    fields = [
        'strategy'
    ]

    list_display = [
        'strategy'
    ]

class InputFilter(admin.SimpleListFilter):
    template = 'admin/input_filter.html'

    def lookups(self, request, model_admin):
        # Dummy, required to show the filter.
        return ((),)

    def choices(self, changelist):
        # Grab only the "all" option.
        all_choice = next(super().choices(changelist))
        all_choice['query_parts'] = (
            (k, v)
            for k, v in changelist.get_filters_params().items()
            if k != self.parameter_name
        )
        yield all_choice

class NameFilter(InputFilter):
    parameter_name = 'name'
    title = 'Name'

    def queryset(self, request, queryset):
        if self.value() is not None:
            name = self.value()

            return queryset.filter(
                name__contains=name
            )

class FormTemplateAdmin(ExportActionMixin, admin.ModelAdmin):
    pass
    list_filter = (NameFilter,)

    list_display = (
        "name",
        "start_date",
        "end_date",
        "target_audience_disciplines",
        "target_audience_roles",
        "implement_strategy_description",
        "consider_system_factors",
        "consider_org_factors",
        "consider_clinical_factors",
        "consider_sustainment_strategy",
        "outcome_reach",
        "outcome_effectiveness",
        "outcome_adoption",
        "outcome_quality",
        "outcome_cost",
        "outcome_other",
        "evaluation_planned_enrollment_organization",
        "evaluation_planned_enrollment_individual",
        "evaluation_enrolled_organization",
        "evaluation_enrolled_individual",
        "evaluation_percent_init_implementation_strategy_organization",
        "evaluation_percent_init_implementation_strategy_individual",
        "evaluation_percent_complete_50_strategy_organization",
        "evaluation_percent_complete_50_strategy_individual",
        "evaluation_percent_complete_80_strategy_organization",
        "evaluation_percent_complete_80_strategy_individual",
        "results_reach",
        "results_effectiveness",
        "results_adoption",
        "results_quality",
        "results_cost",
        "results_other",
    )



admin.site.register(Strategy, StrategyAdmin)
admin.site.register(StrategyType, StrategyTypeAdmin)
admin.site.register(Training, TrainingAdmin)
admin.site.register(TrainingParticipant, TrainingParticipantAdmin)
admin.site.register(FormTemplate, FormTemplateAdmin)
admin.site.register(Project, ProjectAdmin)
