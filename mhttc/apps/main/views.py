"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

from django.shortcuts import render, redirect
from django.http import Http404, JsonResponse
from ratelimit.decorators import ratelimit
from mhttc.settings import DOMAIN_NAME
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.forms.models import model_to_dict
from mhttc.apps.users.decorators import user_agree_terms
from django.db.models import CharField, TextField

from mhttc.apps.main.models import Project, Training, TrainingParticipant, Strategy, FormTemplate, StrategyType, \
    TrainingOutcome
from mhttc.apps.users.models import User
from mhttc.settings import VIEW_RATE_LIMIT as rl_rate, VIEW_RATE_LIMIT_BLOCK as rl_block
from mhttc.apps.main.forms import (
    ProjectForm,
    TrainingForm,
    FormTemplateForm,
    CertificateForm,
)
from mhttc.apps.users.models import Center
from mhttc.apps.main.utils import make_certificate_response
import re
import base64
from django.db.models import Q
from functools import reduce
import operator
from io import BytesIO, StringIO
from xhtml2pdf import pisa

## Projects


@ratelimit(key="ip", rate=rl_rate, block=rl_block)
@login_required
@user_agree_terms
def project_details(request, uuid):
    """Return a project, or 404."""
    try:
        project = Project.objects.get(uuid=uuid)
        return render(
            request, "projects/project_details.html", context={"project": project}
        )
    except Project.DoesNotExist:
        raise Http404


@ratelimit(key="ip", rate=rl_rate, block=rl_block)
@login_required
@user_agree_terms
def user_projects(request):
    """Return a user listing of projects"""
    projects = None
    if request.user.center is not None:
        projects = Project.objects.filter(center=request.user.center)
    return all_projects(request, projects)


@ratelimit(key="ip", rate=rl_rate, block=rl_block)
@login_required
@user_agree_terms
def all_projects(request, projects=None):
    """Return a project, or 404."""
    if projects is None:
        projects = Project.objects.all()
    return render(request, "projects/all_projects.html", context={"projects": projects})


@ratelimit(key="ip", rate=rl_rate, block=rl_block)
@login_required
@user_agree_terms
def new_project(request):
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.center = request.user.center
            project.save()
            return redirect("project_details", uuid=project.uuid)
    else:
        form = ProjectForm()
    return render(request, "projects/new_project.html", {"form": form})


@ratelimit(key="ip", rate=rl_rate, block=rl_block)
@login_required
@user_agree_terms
def delete_project(request, uuid):
    """delete a training event"""
    try:
        project = Project.objects.get(uuid=uuid)
    except Training.DoesNotExist:
        raise Http404

    # Only allowed to edit for their center
    if request.user.center != project.center:
        messages.warning(request, "You are not allowed to perform this action.")
        return redirect("center_events")

    # Delete the training
    project.delete()
    messages.info(request, "Project %s has been deleted." % project.name)
    return redirect("user_projects")


@ratelimit(key="ip", rate=rl_rate, block=rl_block)
@login_required
@user_agree_terms
def search_project(request):
    projects = None
    term = ""

    if request.method == "POST":
        term = request.POST['term']
        words = term.split(" ")
        fields = [f for f in FormTemplate._meta.fields if isinstance(f, TextField)]
        queries = [reduce(operator.or_, (Q(**{f.name + "__icontains": x}) for x in words)) for f in fields]
        qs = Q()
        for query in queries:
            qs = qs | query
        forms_list = FormTemplate.objects.filter(qs).values_list('uuid')
        projects = Project.objects.filter(form_id__in=forms_list, status=Project.PUBLISHED)
        # projects = Project.objects.filter(reduce(operator.or_, (Q(name__contains=x) for x in words))| reduce(operator.or_, (Q(description__contains=x) for x in words)), status=Project.PUBLISHED)
    else:
        projects = Project.objects.filter(status=Project.PUBLISHED)
    return render(request, "projects/search_projects.html",
                  {"projects": projects, 'term': term, 'hide_edit': True, 'center_column': True})


@ratelimit(key="ip", rate=rl_rate, block=rl_block)
@login_required
@user_agree_terms
def publish_project(request, uuid):
    try:
        project = Project.objects.get(uuid=uuid)
    except Project.DoesNotExist:
        raise Http404

    project.status = Project.PUBLISHED
    project.save()
    messages.info(request, "This project is published.")
    return redirect("user_projects")


## Form Templates


@ratelimit(key="ip", rate=rl_rate, block=rl_block)
@login_required
@user_agree_terms
def edit_form_template(request, uuid, stage=1):
    """edit a form template, meaning entering information for different stages"""
    try:
        project = Project.objects.get(uuid=uuid)
    except Project.DoesNotExist:
        raise Http404

    # If a post is done, a JSONresponse must be returned to update the user
    if request.method == "POST":

        # If the form already belongs to another center.

        # Get standard form fields
        form = FormTemplateForm(request.POST)
        form.stage = project.stage
        old_strategies = []
        old_training_outcome = []
        old_form = []
        if form.is_valid():
            if project.form is not None:
                old_form = FormTemplate.objects.get(uuid=project.form_id)
                old_strategies = old_form.implement_strategy.all()
                old_training_outcome = old_form.evaluation_proximal_training_outcome.all()

            template = form.save(commit=False)
            template.save()

            # Also get strategy_ and training_outcome_ fields
            strategy = {}
            training_outcome = {}
            indices = set()
            indices_training_outcome = set()
            for key in request.POST:
                if key.startswith("strategy_"):
                    strategy[key] = request.POST[key]
                    indices.add(key.split("_")[-1])
                if key.startswith("training_outcome_"):
                    training_outcome[key] = request.POST[key]
                    indices_training_outcome.add(key.split("_")[-1])

            new_training_outcomes = []
            try:
                for index in indices_training_outcome:
                    for field in ["outcome", "measure", "results"]:
                        if "training_outcome_%s_%s" % (field, index) not in training_outcome:
                            continue

                    training_outcome_outcome = training_outcome["training_outcome_outcome_%s" % index].strip()
                    training_outcome_measure = training_outcome["training_outcome_measure_%s" % index].strip()


                    if not training_outcome_outcome and not training_outcome_measure:
                        continue

                    if "training_outcome_results_%s" % index in training_outcome:
                        training_outcome_results = training_outcome["training_outcome_results_%s" % index].strip()
                        new_training_outcome = TrainingOutcome.objects.create(
                            outcome=training_outcome_outcome,
                            how_outcome_measured=training_outcome_measure,
                            outcome_results=training_outcome_results
                        )
                    else:
                        new_training_outcome = TrainingOutcome.objects.create(
                            outcome=training_outcome_outcome,
                            how_outcome_measured=training_outcome_measure
                        )

                    new_training_outcomes.append(new_training_outcome)

                # If we have new strategies, remove all
                if new_training_outcomes:
                    [x.delete() for x in old_training_outcome]
                    [template.evaluation_proximal_training_outcome.add(x) for x in new_training_outcomes]
                    template.save()
            except Exception as e:
                project.form = template
                project.save()
                return JsonResponse({"message": "Could not save Training" + str(e)})

            # For each index, only add if all fields are defined
            new_strategies = []
            try:
                for index in indices:
                    for field in ["type", "format", "units", "frequency", "brief_description"]:
                        if "strategy_%s_%s" % (field, index) not in strategy:
                            continue

                    strategy_brief_description = ''
                    # Clean all units
                    strategy_type = strategy["strategy_type_%s" % index].strip()
                    strategy_format = strategy["strategy_format_%s" % index].strip()
                    strategy_units = strategy["strategy_units_%s" % index].strip()
                    strategy_frequency = strategy["strategy_frequency_%s" % index].strip()
                    strategy_brief_description = strategy["strategy_brief_description_%s" % index].strip()

                    if (
                            not strategy_type
                            and not strategy_format
                            and not strategy_units
                            and not strategy_frequency
                    ):
                        continue

                    new_strategy = Strategy.objects.create(
                        strategy_type_id=strategy_type,
                        strategy_format=strategy_format,
                        brief_description=strategy_brief_description,
                        planned_number_units=strategy_units
                        if strategy_units
                        else None,
                        frequency=strategy_frequency,
                    )
                    new_strategies.append(new_strategy)

                # If we have new strategies, remove all
                if new_strategies:
                    for test in old_strategies:
                        yy = test.delete()
                    # [x.delete() for x in old_strategies]
                    [template.implement_strategy.add(x) for x in new_strategies]
                    template.save()
            except Exception as e:
                project.form = template
                project.save()
                return JsonResponse({"message": "Could not save Strategy" + str(e)})


            # Unless we are at stage 3, add 1 to stage
            if 'next-stage' in request.POST and request.POST['next-stage'] == 'on':
                if project.stage != 3 and project.stage <= 3:
                    project.stage += 1
                    form.stage = project.stage
            project.form = template
            project.save()
            try:
                old_form.delete()
            except:
                return JsonResponse({"message": "Your project was saved successfully."})
            return JsonResponse({"message": "Your project was saved successfully."})

        # Not valid - return to page to populate
        else:
            return JsonResponse(
                {"message": "The form is not valid, errors: %s" % form.errors}
            )
    else:
        form = FormTemplateForm()
        if project.form is not None:
            form = FormTemplateForm(initial=model_to_dict(project.form))
        form.stage = project.stage

    strategies = None
    if project.form is not None and project.form.implement_strategy is not None:
        strategies = project.form.implement_strategy.all()
 

    training_outcomes = None
    if project.form is not None and project.form.evaluation_proximal_training_outcome is not None:
        training_outcomes = project.form.evaluation_proximal_training_outcome.all()

    return render(
        request,
        "projects/edit_form_template.html",
        {
            "form": form,
            "project": project,
            "strategies": strategies,
            "strategies_types": StrategyType.objects.all().order_by('strategy'),
            "training_outcomes": training_outcomes,
        },
    )

from django.http import FileResponse, HttpResponse
import os
from django.conf import settings
@ratelimit(key="ip", rate=rl_rate, block=rl_block)
@login_required
@user_agree_terms
def download_form_pdf(request, file_name):
    with open(os.path.join(settings.STATIC_ROOT, file_name), 'rb') as fh:
        response = HttpResponse(fh.read(), content_type="application/pdf")
        response['Content-Disposition'] = 'attachment; filename=' + file_name
        return response

@ratelimit(key="ip", rate=rl_rate, block=rl_block)
@login_required
@user_agree_terms
def generate_form_pdf(request, uuid):
    try:
        project = Project.objects.get(uuid=uuid)
        if request.method == "POST":
            if 'content' not in request.POST:
                raise Exception("Content is missing")
            html = str(request.POST['content'])
            result_file = open('/static/' + str(uuid) + '.pdf', "w+b")
            pisa_status = pisa.pisaDocument(BytesIO(html.encode("UTF-8"))
                ,  # the HTML to convert
                dest=result_file)  # file handle to recieve result
            return JsonResponse(
                {"status": "success",  "path": str(uuid) + '.pdf'}
            )
        else:
            raise Exception("Method is wrong")
    except Project.DoesNotExist:
        raise Http404
    except Exception as e:
        return JsonResponse(
            {"message": str(e)}
        )



@ratelimit(key="ip", rate=rl_rate, block=rl_block)
@login_required
@user_agree_terms
def view_project_form(request, uuid):
    try:
        project = Project.objects.get(uuid=uuid)

        form = FormTemplateForm()
        if project.form is not None:
            form = FormTemplateForm(initial=model_to_dict(project.form))

        # If the form already belongs to another center
        # if project.center != None and project.center != request.user.center:
        #     messages.warning(
        #         request,
        #         "You are not allowed to edit a form not owned by your center.",
        #     )
        #     return redirect("index")

        # If the form isn't started yet...
        if project.form == None:
            messages.info(request, "This project does not have a form started yet.")
            return redirect("project_details", project.uuid)

        training_outcomes = None
        if project.form is not None and project.form.evaluation_proximal_training_outcome is not None:
            training_outcomes = project.form.evaluation_proximal_training_outcome.all()

        return render(
            request,
            "projects/view_project_form.html",
            context={
                "project": project,
                "form": form,
                "disabled": True,
                "training_outcomes": training_outcomes,
                "strategies_types": StrategyType.objects.all().order_by('strategy'),
                "strategies": project.form.implement_strategy.all(),
            },
        )
    except Project.DoesNotExist:
        raise Http404


## Events


@ratelimit(key="ip", rate=rl_rate, block=rl_block)
@login_required
@user_agree_terms
def new_event(request):
    """Create a new event. A user that does not have full access to the site
    cannot see this view
    """
    if not request.user.center.full_access:
        messages.warning(request, "You are not allowed to perform this action.")
        return redirect("index")

    if request.method == "POST":
        form = TrainingForm(request.POST, request.FILES)

        # Parse base64 string to save to database
        encoded_string = base64.b64encode(request.FILES["file"].read()).decode("utf-8")

        title = request.POST['name'].encode("ascii", errors="ignore").decode()
        description = request.POST['description'].encode("ascii", errors="ignore").decode()
        if form.is_valid():
            training = form.save(commit=False)
            training.contact = User.objects.get(id=int(request.POST['contact'])) if request.POST['contact'] else None
            training.lead = User.objects.get(id=int(request.POST['lead'])) if request.POST['lead'] else None
            training.center = request.user.center
            training.image_data = encoded_string
            training.name = title
            training.description = description
            training.save()
            return redirect("event_details", uuid=training.uuid)
    else:
        form = TrainingForm()
    return render(request, "events/new_event.html", {"form": form})


@ratelimit(key="ip", rate=rl_rate, block=rl_block)
@login_required
@user_agree_terms
def center_events(request):
    """Return a listing of events being held by the center. A user
    that does not have full access to the site cannot see this view.
    """
    if not request.user.center.full_access:
        messages.warning(request, "You are not allowed to perform this action.")
        return redirect("index")

    if not request.user.center:
        messages.info(request, "You are not part of a center.")
        redirect("index")
    events = Training.objects.filter(center=request.user.center)
    return render(
        request,
        "events/center_events.html",
        {"events": events, "center": request.user.center},
    )


@ratelimit(key="ip", rate=rl_rate, block=rl_block)
@login_required
@user_agree_terms
def event_details(request, uuid):
    """Return the details of an event. A user that does not have full access
    to the site cannot see this view.
    """
    if not request.user.center.full_access:
        messages.warning(request, "You are not allowed to perform this action.")
        return redirect("index")

    try:
        training = Training.objects.get(uuid=uuid)
        edit_permission = training.center == request.user.center

        if request.method == "POST":

            # Only allowed to edit for their center
            if (
                    request.user.center != training.center
                    or not request.user.center.full_access
            ):
                messages.warning(request, "You are not allowed to perform this action.")
                return redirect("center_events")

            # Can only send if there is an associated image data
            if training.image_data in [None, ""]:
                messages.info(
                    request,
                    "You must upload a certificate template before sending certificates.",
                )
                return redirect("event_details", uuid=training.uuid)

            # Add new participant emails
            emails = request.POST.get("emails", "")
            count = 0
            for email in emails.split("\n"):

                # Any weird newlines
                email = email.strip()

                # Skip empty lines
                if not email:
                    continue

                # Allow user to provide an email copy pasted with name <email>
                match = re.search(
                    "([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})", email
                )
                if not match:
                    continue
                email = match.group()

                participant, created = TrainingParticipant.objects.get_or_create(
                    training=training, email=email
                )
                participant.save()
                participant.send_certificate(training=training)
                count += 1

            # Tell the user how many were sent
            messages.info(
                request, "You have requested %s certificate emails to be sent." % count
            )

        generation_url =   "%s%s" % (
            DOMAIN_NAME,
            reverse("download_certificate", args=[training.uuid]),
        )

        return render(
            request,
            "events/event_details.html",
            context={"training": training, "edit_permission": edit_permission, "generation_url": generation_url},
        )
    except Training.DoesNotExist:
        raise Http404


@ratelimit(key="ip", rate=rl_rate, block=rl_block)
@login_required
@user_agree_terms
def update_event_image(request, uuid):
    """update the image for an event."""
    if request.method == "POST":

        try:
            training = Training.objects.get(uuid=uuid)
        except Training.DoesNotExist:
            raise Http404

        # Only allowed to edit for their center
        if request.user.center != training.center:
            messages.warning(request, "You are not allowed to perform this action.")
            return redirect("center_events")

        training.image_data = base64.b64encode(request.FILES["file"].read()).decode(
            "utf-8"
        )
        training.save()

    return redirect("event_details", uuid=training.uuid)


@ratelimit(key="ip", rate=rl_rate, block=rl_block)
@login_required
@user_agree_terms
def edit_event(request, uuid):
    """edit event details"""
    try:
        training = Training.objects.get(uuid=uuid)
    except Training.DoesNotExist:
        raise Http404

    # Only allowed to edit for their center
    if request.user.center != training.center:
        messages.warning(request, "You are not allowed to perform this action.")
        return redirect("center_events")

    if request.method == "POST":

        # Do we have updated image data?
        encoded_string = training.image_data
        if "file" in request.FILES:
            encoded_string = base64.b64encode(request.FILES["file"].read()).decode(
                "utf-8"
            )

        form = TrainingForm(request.POST, request.FILES, instance=training)
        if form.is_valid():
            training = form.save(commit=False)
            training.center = request.user.center
            training.contact = User.objects.get(id=(int(request.POST['contact']))) if request.POST['contact'] else None
            training.lead = User.objects.get(id=int(request.POST['lead'])) if request.POST['lead'] else None
            training.image_data = encoded_string
            training.save()
            return redirect("event_details", uuid=training.uuid)

        # Form errors
        else:
            return render(request, "events/new_event.html", {"form": form})
    else:
        form = TrainingForm(initial=model_to_dict(training, fields=[field.name for field in training._meta.fields]))
        
    return render(request, "events/edit_event.html", {"form": form})


@ratelimit(key="ip", rate=rl_rate, block=rl_block)
@login_required
@user_agree_terms
def delete_event(request, uuid):
    """delete a training event"""
    try:
        training = Training.objects.get(uuid=uuid)
    except Training.DoesNotExist:
        raise Http404

    # Only allowed to edit for their center
    if request.user.center != training.center:
        messages.warning(request, "You are not allowed to perform this action.")
        return redirect("center_events")

    # Delete the training
    training.delete()
    messages.info(request, "Event %s has been deleted." % training.name)
    return redirect("center_events")


@csrf_exempt
def download_certificate(request, uuid):
    """download a certificate for an event."""
    try:
        training = Training.objects.get(uuid=uuid)
    except Training.DoesNotExist:
        raise Http404

    form = CertificateForm()
    if request.method == "POST":
        form = CertificateForm(request.POST)
        if form.is_valid():

            # Ensure that the participant is completed for the training
            email = form.cleaned_data["email"]
            try:
                participant = TrainingParticipant.objects.get(email=email, training=training)
                participant.name = request.POST['name']
                participant.save()
            except:
                messages.warning(
                    request, "We cannot find a record of your participation."
                )
                return render(
                    request,
                    "events/download_certificate.html",
                    {"form": form, "training": training},
                )

            # Create temporary image (cleaned up from /tmp when container rebuilt weekly)
            image_path = training.get_temporary_image()
            return make_certificate_response(
                form.cleaned_data["name"],
                training,
                image_path,
            )
        else:
            messages.warning(request, "Your form submission is not valid.")

    u = request.user
    if u.id == None:
        hide_login = True
    else:
        hide_login = False

    return render(
        request,
        "events/download_certificate.html",
        {"form": form, "training": training, "hide_login": hide_login},
    )
