from django import template
from mhttc.apps.main.models import Project
from mhttc.apps.users.models import Center
register = template.Library()

def can_edit(project, request):
    # check if user if part of center

    return True

def can_view(project, request):

    # check if user if part of center
    # if Center.is_user_part_of_center(project.center, request.user):
    #     return True

    return True

def can_publish(project, request):
    if project.center != None and project.center != request.user.center:
        return False
    return True


register.filter('can_edit', can_edit)
register.filter('can_view', can_view)
register.filter('can_publish', can_publish)
