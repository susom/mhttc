"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
from django.db.models import Q
from django.contrib import admin
from mhttc.apps.main.models import Project, FormTemplate, Training, TrainingParticipant, StrategyType, Strategy
from import_export import resources
from import_export.fields import Field
from import_export.widgets import ForeignKeyWidget
from import_export.admin import ExportActionMixin


class FormTemplateResource(resources.ModelResource):
    project_name = Field()
    project_stage = Field()
    project_status = Field()
    project_center = Field()
    implement_strategy_1 = Field(column_name='implement_strategy_1')
    implement_strategy_2 = Field(column_name='implement_strategy_2')
    implement_strategy_3 = Field(column_name='implement_strategy_3')
    implement_strategy_4 = Field(column_name='implement_strategy_4')
    implement_strategy_5 = Field(column_name='implement_strategy_5')
    implement_strategy_6 = Field(column_name='implement_strategy_6')
    implement_strategy_7 = Field(column_name='implement_strategy_7')
    implement_strategy_8 = Field(column_name='implement_strategy_8')
    implement_strategy_9 = Field(column_name='implement_strategy_9')
    implement_strategy_10 = Field(column_name='implement_strategy_10')

    training_outcome_1 = Field(column_name='training_outcome_1')
    training_outcome_2 = Field(column_name='training_outcome_2')
    training_outcome_3 = Field(column_name='training_outcome_3')
    training_outcome_4 = Field(column_name='training_outcome_4')
    training_outcome_5 = Field(column_name='training_outcome_5')
    training_outcome_6 = Field(column_name='training_outcome_6')
    training_outcome_7 = Field(column_name='training_outcome_7')
    training_outcome_8 = Field(column_name='training_outcome_8')
    training_outcome_9 = Field(column_name='training_outcome_9')
    training_outcome_10 = Field(column_name='training_outcome_10')


    class Meta:
        model = FormTemplate
        export_order = ('uuid',
                  'project_name',
                  'project_stage',
                  'project_status',
                  'project_center',
                  'implement_strategy_1',
                  'implement_strategy_2',
                  'implement_strategy_3',
                  'implement_strategy_4',
                  'implement_strategy_5',
                  'implement_strategy_6',
                  'implement_strategy_7',
                  'implement_strategy_8',
                  'implement_strategy_9',
                  'implement_strategy_10',
                  'training_outcome_1',
                  'training_outcome_2',
                  'training_outcome_3',
                  'training_outcome_4',
                  'training_outcome_5',
                  'training_outcome_6',
                  'training_outcome_7',
                  'training_outcome_8',
                  'training_outcome_9',
                  'training_outcome_10',
                  'time_created',
                  'time_updated',
                  'start_date',
                  'end_date',
                  'name',
                  'need',
                  'target_audience_settings',
                  'target_audience_disciplines',
                  'target_audience_roles',
                  'target_audience_relations',
                  'target_audience_relations_other',
                  'target_audience_ta_recipients',
                  'consider_system_factors', 'consider_org_factors',
                  'consider_clinical_factors',
                  'consider_system_factors_barriers',
                  'consider_org_factors_barriers',
                  'consider_clinical_factors_barriers',
                  'consider_ascertained',
                  'consider_sustainment_strategy',
                  'implement_strategy_description',
                  'evaluation_planned_enrollment_organization',
                  'evaluation_planned_enrollment_individual',
                  'evaluation_proximal_training_outcome',
                  'evaluation_enrolled_organization',
                  'evaluation_enrolled_individual',
                  'evaluation_percent_init_implementation_strategy_organization',
                  'evaluation_percent_init_implementation_strategy_individual',
                  'evaluation_percent_complete_50_strategy_organization',
                  'evaluation_percent_complete_50_strategy_individual',
                  'evaluation_percent_complete_80_strategy_organization',
                  'evaluation_percent_complete_80_strategy_individual',
                  'outcome_reach',
                  'outcome_effectiveness',
                  'outcome_adoption',
                  'outcome_quality',
                  'outcome_cost',
                  'outcome_maintenance',
                  'outcome_other',
                  'results_reach',
                  'results_effectiveness',
                  'results_adoption',
                  'results_quality',
                  'results_cost',
                  'results_maintenance',
                  'results_other',
                  'other_relevant_issues')
        exclude = ('implementation_completing_half', 'implementation_completing_majority')

    def dehydrate_project_name(self, form):
        try:
            project = Project.objects.get(form_id=form.uuid)
            return '%s' % (project.name)
        except Project.DoesNotExist:
            return 'No Project Found'

    def dehydrate_project_center(self, form):
        try:
            project = Project.objects.get(form_id=form.uuid)
            return '%s' % (project.center.name)
        except Project.DoesNotExist:
            return 'No Project Found'

    def dehydrate_project_stage(self, form):
        try:
            project = Project.objects.get(form_id=form.uuid)
            return '%s' % (project.stage)
        except Project.DoesNotExist:
            return ''

    def dehydrate_project_status(self, form):
        try:
            project = Project.objects.get(form_id=form.uuid)
            if project.status == Project.DRAFT:
                return 'Draft'
            else:
                return 'Published'
        except Project.DoesNotExist:
            return ''

    def dehydrate_implement_strategy_1(self, form):
        return self.get_form_strategy_via_index(form, 0, 1)

    def dehydrate_implement_strategy_2(self, form):
        return self.get_form_strategy_via_index(form, 1, 2)

    def dehydrate_implement_strategy_3(self, form):
        return self.get_form_strategy_via_index(form, 2, 3)

    def dehydrate_implement_strategy_4(self, form):
        return self.get_form_strategy_via_index(form, 3, 4)

    def dehydrate_implement_strategy_5(self, form):
        return self.get_form_strategy_via_index(form, 4, 5)

    def dehydrate_implement_strategy_6(self, form):
        return self.get_form_strategy_via_index(form, 5, 6)

    def dehydrate_implement_strategy_7(self, form):
        return self.get_form_strategy_via_index(form, 6, 7)

    def dehydrate_implement_strategy_8(self, form):
        return self.get_form_strategy_via_index(form, 7, 8)

    def dehydrate_implement_strategy_9(self, form):
        return self.get_form_strategy_via_index(form, 8, 9)

    def dehydrate_implement_strategy_10(self, form):
        return self.get_form_strategy_via_index(form, 9, 10)


    def dehydrate_training_outcome_1(self, form):
        return self.get_form_training_outcome_via_index(form, 0, 1)

    def dehydrate_training_outcome_2(self, form):
        return self.get_form_training_outcome_via_index(form, 1, 2)

    def dehydrate_training_outcome_3(self, form):
        return self.get_form_training_outcome_via_index(form, 2, 3)

    def dehydrate_training_outcome_4(self, form):
        return self.get_form_training_outcome_via_index(form, 3, 4)

    def dehydrate_training_outcome_5(self, form):
        return self.get_form_training_outcome_via_index(form, 4, 5)

    def dehydrate_training_outcome_6(self, form):
        return self.get_form_training_outcome_via_index(form, 5, 6)

    def dehydrate_training_outcome_7(self, form):
        return self.get_form_training_outcome_via_index(form, 6, 7)

    def dehydrate_training_outcome_8(self, form):
        return self.get_form_training_outcome_via_index(form, 7, 8)

    def dehydrate_training_outcome_9(self, form):
        return self.get_form_training_outcome_via_index(form, 8, 9)

    def dehydrate_training_outcome_10(self, form):
        return self.get_form_training_outcome_via_index(form, 9, 10)

    @staticmethod
    def get_form_strategy_via_index(form, start, end):
        try:
            field = ''
            strategies = form.implement_strategy.all().order_by('-time_created')[start:end]
            for strategy in strategies:
                field += strategy.strategy_type.strategy + ', '
            if field != '':
                return '%s' % (field[:-2])
            else:
                return ''
        except Strategy.DoesNotExist:
            return ''

    @staticmethod
    def get_form_training_outcome_via_index(form, start, end):
        try:
            field = ''
            outcomes = form.evaluation_proximal_training_outcome.all().order_by('-id')[start:end]
            for outcome in outcomes:
                field += outcome.outcome + ', '
            if field != '':
                return '%s' % (field[:-2])
            else:
                return ''
        except Strategy.DoesNotExist:
            return ''

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
        'categories',
        'strategy',
        'active'
    ]

    list_display = [
        'categories',
        'strategy',
        'active'
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

    resource_class = FormTemplateResource
    list_display = (
        "project_name",
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

    def project_name(self, form):
        try:
            project = Project.objects.get(form_id=form.uuid)
            return '%s' % (project.name)
        except Project.DoesNotExist:
            return 'No Project Found'


admin.site.register(Strategy, StrategyAdmin)
admin.site.register(StrategyType, StrategyTypeAdmin)
admin.site.register(Training, TrainingAdmin)
admin.site.register(TrainingParticipant, TrainingParticipantAdmin)
admin.site.register(FormTemplate, FormTemplateAdmin)
admin.site.register(Project, ProjectAdmin)
