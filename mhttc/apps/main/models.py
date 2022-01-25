"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

from mhttc.settings import DOMAIN_NAME, SENDGRID_SENDER_EMAIL
from django.db import models
from django.urls import reverse
import base64
import tempfile
import uuid
from mhttc.apps.users.models import User

class Training(models.Model):
    """A training holds one or more participants and a certificate template to give
    on completion
    """

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Why do these fields use time, and others use date (e.g., see ip_check*)
    time_created = models.DateTimeField("date created", auto_now_add=True)
    time_updated = models.DateTimeField("date modified", auto_now=True)
    name = models.CharField(max_length=250, blank=False)
    image_data = models.TextField(null=True, blank=True)
    image_url = models.URLField(
        max_length=500,
        blank=True,
        null=True,
        help_text="Leave this blank to use the default template.",
    )
    description = models.CharField(max_length=500, blank=True, null=True)

    # I suggested a start and end date time here, but Heather explicitly asked for a
    # blank text field for dates, since will be widely varying in format
    dates = models.CharField(max_length=250, blank=True, null=True)
    duration = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="duration with units (typically hours)",
    )

    # A project must be owned by a center, and the contact must be a user
    center = models.ForeignKey("users.Center", on_delete=models.PROTECT, blank=False)
    contact = models.ForeignKey(
        "users.User", on_delete=models.PROTECT, blank=True, null=True
    )

    lead = models.ForeignKey("users.User", on_delete=models.PROTECT, related_name='lead', blank=True, null=True)

    @property
    def slug(self):
        return self.name.replace(" ", "-").lower()

    def deslugify(self, name):
        return name.replace("-", " ")

    def __str__(self):
        return "<Training:%s>" % self.name

    def get_temporary_image(self):
        """Given image data, write a temporary image to file to generate certificate."""
        _, image_path = tempfile.mkstemp(prefix="training-template", suffix=".png")
        image_data = base64.b64decode(self.image_data)
        with open(image_path, "wb") as fh:
            fh.write(image_data)
        return image_path

    def get_absolute_url(self):
        return reverse("event_details", args=[self.uuid])

    def get_label(self):
        return "training"

    class Meta:
        app_label = "main"
        unique_together = [["name", "center", "dates"]]


class TrainingParticipant(models.Model):
    """A training participant is an email address (and status?) to indicate
    the status for a participant.
    """

    name = models.CharField(max_length=250, blank=False)
    email = models.CharField(max_length=100, blank=True, null=True)
    training = models.ForeignKey("main.Training", on_delete=models.CASCADE, blank=False)

    def send_certificate(self, training):
        """Given a training, send a user a certificate"""
        from mhttc.apps.users.utils import send_email

        url = "%s%s" % (
            DOMAIN_NAME,
            reverse("download_certificate", args=[training.uuid]),
        )

        # This is in html
        message = (
                "Thank you for attending the event '%s' from the Mental Health Technology Transfer Center (MHTTC) Network!<br>"
                "You can visit <a href='%s'>the certificate download page</a> to get your certificate.<br><br>"
                "If this message was in error, please respond to this email and let us know.<br><br>"
                "Be sure to look for more of our events at www.mhttcnetwork.org and find "
                " your MHTTC Regional or National Focus Area Center at https://mhttcnetwork.org/centers/selection"
                % (training.name, url)
        )
        if send_email(
                email_to=self.email,
                email_from=self.training.center.email or SENDGRID_SENDER_EMAIL,
                message=message,
                subject="Your event certificate of completion is ready!",
        ):
            self.save()

    def get_absolute_url(self):
        return reverse("participant_details", args=[self.uuid])

    def get_label(self):
        return "training_participant"

    class Meta:
        app_label = "main"
        unique_together = [["email", "training"]]


class Project(models.Model):
    """A project is owned by a center, and includes one or more form templates."""

    DRAFT = 0
    PUBLISHED = 1

    PUBLIC = 0
    PRIVATE = 1

    STATUS_CHOICES = (
        (DRAFT, 'Draft'),
        (PUBLISHED, 'Published')
    )

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Why do these fields use time, and others use date (e.g., see ip_check*)
    time_created = models.DateTimeField("date created", auto_now_add=True)
    time_updated = models.DateTimeField("date modified", auto_now=True)
    name = models.CharField(max_length=250, blank=False, verbose_name='Project Title')
    description = models.CharField(max_length=500, blank=True, null=True)
    stage = models.PositiveIntegerField(default=1)

    status = models.IntegerField(choices=STATUS_CHOICES, default=0, null=False, blank=True)

    # Manage project forms
    form = models.ForeignKey(
        "main.FormTemplate", on_delete=models.CASCADE, blank=True, null=True
    )

    # A project must be owned by a center, and the contact must be a user
    center = models.ForeignKey("users.Center", on_delete=models.PROTECT, blank=False)
    contact = models.ForeignKey("users.User", on_delete=models.PROTECT, blank=False)

    @property
    def stage_label(self):
        if self.stage == 1:
            return 'Exploratory/Planning Phase'
        elif self.stage == 2:
            return 'Implementation Phase'
        elif self.stage == 3:
            return 'Sustainment Phase'
        else:
            raise Exception('Unknown Stage')

    def get_absolute_url(self):
        return reverse("project_details", args=[self.uuid])

    def get_label(self):
        return "project"

    class Meta:
        app_label = "main"


class StrategyType(models.Model):
    """An implementation strategy types to add to a Strategy"""

    TYPES_CATEGORIES = (
        (1, 'Change infrastructure'),
        (2, 'Use financial strategies'),
        # (3, 'Engage consumers'),
        (4, 'Support deliverers of the intervention/program/service'),
        (5, 'Train and educate stakeholders'),
        (6, 'Develop stakeholder relationships'),
        (7, 'Adapt and tailor content'),
        (8, 'Provide interactive assistance'),
        (9, 'Use evaluative and iterative strategies'),
        (0, 'Other'),
    )

    categories = models.PositiveIntegerField(choices=TYPES_CATEGORIES, default=0, null=False, blank=False)

    strategy = models.CharField(max_length=500, blank=True, null=True, help_text="Category")

    active = models.BooleanField(default=True, null=False, blank=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True,
                                   related_name="strategy_type_created_by")
    created_at = models.DateTimeField("date created", auto_now_add=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True,
                                   related_name="strategy_type_updated_by")
    updated_at = models.DateTimeField("date modified", auto_now=True)

    def get_label(self):
        return "strategy_type"

    def __str__(self):
        return self.strategy

    class Meta:
        app_label = "main"

    @staticmethod
    def get_types_grouped_by_categories():
        result = {}
        for category in StrategyType.TYPES_CATEGORIES:

            result[category[1]] = list(StrategyType.objects.filter(categories=category[0]).values())

        return result


class Strategy(models.Model):
    """An implementation strategy to add to a FormTemplate"""

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    time_created = models.DateTimeField("date created", auto_now_add=True)
    time_updated = models.DateTimeField("date modified", auto_now=True)

    frequency = models.CharField(max_length=250, blank=False, help_text="Frequency")
    strategy_format = models.CharField(
        max_length=500, blank=True, null=True, help_text="Format"
    )
    # strategy_type = models.CharField(
    #     max_length=500, blank=True, null=True, help_text="Category"
    # )
    strategy_type = models.ForeignKey(StrategyType, on_delete=models.CASCADE, null=True, blank=True,
                                      related_name="strategy_type")

    planned_number_units = models.CharField(max_length=500, blank=True, null=True,
        help_text="Planned number of units"
    )

    brief_description = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.brief_description)

    def get_label(self):
        return "strategy"

    class Meta:
        app_label = "main"


class TrainingOutcome(models.Model):
    '''
    capture evaluation training outcome
    '''
    outcome = models.TextField(null=True, blank=True)
    how_outcome_measured = models.TextField(null=True, blank=True)
    outcome_results = models.TextField(null=True, blank=True)


class FormTemplate(models.Model):
    """A form template collects basic information about the project. We render
    different information and make it editable for the user depending on their
    role and the project stage.
    """

    RELATIONSHIP_CHOICES = (
        (1, 'Single individuals from multiple organizations'),
        (2, 'Multiple individuals within one organization'),
        (3, 'Multiple individuals or teams from multiple organizations'),
        (99, 'Other'),
    )

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Create, update (complete) times
    time_created = models.DateTimeField("date created", auto_now_add=True, editable=True)
    time_updated = models.DateTimeField(
        "date modified", auto_now=True, help_text="Template Updated or completed at."
    )

    # Project start / end date
    start_date = models.DateTimeField(blank=False,
                                      null=True, help_text="project start date")
    end_date = models.DateField(blank=False,
                                    null=True, help_text="project end date")

    # 1. Evidence based intervention (what)
    name = models.TextField(
        blank=False,
        help_text="Evidence-Based Intervention/Program/Service Being Implemented (WHAT)",
    )

    # 2. What is the need/rationale for this project?  Why/how did you decide to do this project?
    need = models.TextField(
        blank=False,
        null=True,
        help_text="What is the need/rationale for this project?  Why/how did you decide to do this project?",
    )

    # 3. Target audience/TA recipients (WHO and WHERE)
    target_audience_who = models.TextField(
        blank=False,
        null=True, help_text="Who is the audience (including type of organizations)"
    )

    target_audience_settings = models.TextField(
        blank=False,
        null=True,
        help_text="Specify the audience’s setting (e.g., emergency departments, schools, opioid treatment programs):"
    )
    target_audience_disciplines = models.TextField(
        blank=False,
        null=True, help_text="Specify discipline(s) of individuals: "
    )
    target_audience_roles = models.TextField(blank=False,
                                             null=True, help_text="Specify roles of individuals: ")

    target_audience_relations = models.IntegerField(choices=RELATIONSHIP_CHOICES, default=1, null=False, blank=True,
                                                    help_text="Specify audience relationship to one another (Choose one):")

    target_audience_relations_other = models.TextField(blank=False,
                                                     null=False,
                                                     help_text="If Other, please specify?", default="")

    target_audience_ta_recipients = models.TextField(blank=False,
                                                     null=True,
                                                     help_text="How will your target audience/TA recipients be recruited?")

    # **********************************************************************

    # 4. Contextual/determinant Considerations
    # ************************************************ Facilitators **************************************************
    consider_system_factors = models.TextField(blank=False,
                                               null=True,
                                               help_text="System factors--external to the organization (e.g., financing; mandates, community, culture)"
                                               )
    consider_org_factors = models.TextField(blank=False,
                                            null=True,
                                            help_text="Organizational factors—internal to the organization (e.g., leadership; readiness)"
                                            )
    consider_clinical_factors = models.TextField(blank=False,
                                                 null=True,
                                                 help_text="Individual clinician factors (e.g., alignment with existing practice; complexity)"
                                                 )
    # ************************************************ END Facilitators **************************************************

    # ************************************************ Barriers **************************************************
    consider_system_factors_barriers = models.TextField(blank=False,
                                                        null=True,
                                                        help_text="System factors--external to the organization (e.g., financing; mandates, community, culture)"
                                                        )
    consider_org_factors_barriers = models.TextField(blank=False,
                                                     null=True,
                                                     help_text="Organizational factors—internal to the organization (e.g., leadership; readiness)"
                                                     )
    consider_clinical_factors_barriers = models.TextField(blank=False,
                                                          null=True,
                                                          help_text="Individual clinician factors (e.g., alignment with existing practice; complexity)"
                                                          )
    # ************************************************ END Barriers **************************************************

    consider_ascertained = models.TextField(
        help_text="How were these considerations ascertained (e.g., formal evaluation, needs/readiness assessment)?",
        blank=True, null=True
    )  # only form stage 3

    consider_sustainment_strategy = models.TextField(
        help_text="Sustainment strategies applied", blank=True, null=True
    )  # only form stage 3

    # 5. Implementation strategy
    implement_strategy = models.ManyToManyField(
        "main.Strategy",
        blank=False,
        null=True,
        default=None,
        related_name="form_template1",
        related_query_name="form_template1",
    )

    implement_strategy_description = models.TextField(
        blank=False,
        null=False,
        help_text="Describe the sequence of the planned Implementation Strategies, step by step:",
    )

    # 6. Evaluation
    evaluation_planned_enrollment_organization = models.CharField(max_length=255,
        help_text="How many organization planned for enrollment? (number only)", blank=True, null=True, )
    evaluation_planned_enrollment_individual = models.CharField(max_length=255,
        help_text="How many individual planned for enrollment? (number only)", blank=True, null=True, )

    evaluation_proximal_training_outcome = models.ManyToManyField(
        "main.TrainingOutcome",
        blank=False,
        null=True,
        related_name="form_training_outcome",
        related_query_name="form_training_outcome",
    )
    # 6 Evaluation Stage 2
    evaluation_enrolled_organization = models.IntegerField(help_text="How many organizations enrolled?", blank=True,
                                                           null=True, )
    evaluation_enrolled_individual = models.IntegerField(help_text="How many individuals enrolled?", blank=True,
                                                         null=True, )

    evaluation_percent_init_implementation_strategy_organization = models.FloatField(
        help_text="Percentage of organization initiating implementation strategy", blank=True, null=True, )
    evaluation_percent_init_implementation_strategy_individual = models.FloatField(
        help_text="Percentage of individual initiating implementation strategy", blank=True, null=True, )

    # 6 Evaluation Stage 3
    evaluation_percent_complete_50_strategy_organization = models.FloatField(
        help_text="Percentage of Organization completing 50% of implementation strategy activities: ", blank=True,
        null=True, )
    evaluation_percent_complete_50_strategy_individual = models.FloatField(
        help_text="Percentage of individual completing 50% of implementation strategy activities:", blank=True,
        null=True, )

    evaluation_percent_complete_80_strategy_organization = models.FloatField(
        help_text="Percentage of Organization completing 80% or more of implementation strategy activities: ",
        blank=True, null=True, )
    evaluation_percent_complete_80_strategy_individual = models.FloatField(
        help_text="Percentage of individual completing 80% or more of implementation strategy activities:", blank=True,
        null=True, )

    # 6. Measures being planned (stage 1)
    outcome_reach = models.TextField(blank=False,
                                     null=True,
                                     help_text="Reach (# or percentage of population, what is the population, and how will you be measuring the outcome?"
                                     )
    outcome_effectiveness = models.TextField(blank=False,
                                             null=True,
                                             help_text="Effectiveness of Intervention/Program/Services (w/consumers), how will you measure it?"
                                             )
    outcome_adoption = models.TextField(blank=False,
                                        null=True,
                                        help_text="Number of providers? How will you be measuring it?"
                                        )
    outcome_quality = models.TextField(blank=False,
                                       null=True,
                                       help_text="Implementation Fidelity/Adherence/Quality. How will you be measuring it?"
                                       )
    outcome_cost = models.TextField(blank=False,
                                    null=True, help_text="Cost. How will you keep track of it?")
    outcome_maintenance = models.TextField(blank=False,
                                           null=True, help_text="Maintenance/Sustainment.")
    outcome_other = models.TextField(blank=False,
                                     null=True, help_text="Any other measures being planned?")

    # the following are only for (stage 3)
    implementation_completing_half = models.PositiveIntegerField(
        help_text="# (%) completing 50% of implementation strategy activities",
        blank=True,
        null=True,
    )
    implementation_completing_majority = models.PositiveIntegerField(
        help_text="# (%) completing 80% or more of implementation strategy activities",
        blank=True,
        null=True,
    )

    # 6. Results Available (stage 2)
    results_reach = models.TextField(
        help_text="Reach (# or percentage of population, what is the population, and how will you be measuring the outcome?",
        blank=True,
        null=True,
    )
    results_effectiveness = models.TextField(
        help_text="Effectiveness of Intervention/Program/Services (w/consumers), how will you measure it?",
        blank=True,
        null=True,
    )
    results_adoption = models.TextField(
        help_text="Results available for number of providers?", blank=True, null=True
    )
    results_quality = models.TextField(
        help_text="Results available for implementation Fidelity/Adherence/Quality?",
        blank=True,
        null=True,
    )
    results_cost = models.TextField(
        help_text="Results available for cost?", blank=True, null=True
    )
    results_maintenance = models.TextField(
        help_text="Results for Maintenance/Sustainment.", blank=True, null=True
    )
    results_other = models.TextField(
        help_text="Results available for other?", blank=True, null=True
    )

    # 7 Other relevant issues
    other_relevant_issues = models.TextField(
        help_text="Other relevant issues?", blank=True, null=True
    )

    def __str__(self):
        return str(self.name)


    def get_absolute_url(self):
        return reverse("formtemplate_details", args=[self.uuid])

    def get_label(self):
        return "formtemplate"

    class Meta:
        app_label = "main"
