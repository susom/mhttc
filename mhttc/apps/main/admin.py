"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

from django.contrib import admin
from mhttc.apps.main.models import Project, FormTemplate, Training, TrainingParticipant, StrategyType, Strategy


class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        "name",
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

class FormTemplateAdmin(admin.ModelAdmin):
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
