from django import template
from mhttc.apps.main.models import Project
from mhttc.apps.users.models import Center
register = template.Library()

def can_edit(project, request):
    # # check if user if part of center
    # if Center.is_user_part_of_center(project.center, request.user):
    #     return True
    #
    # # check if user is part of sister center
    # if Center.is_center_part_of_same_group(project.center, request.user.center):
    #     return True

    return True

def can_view(project, request):
    #
    # # if project is marked public then display it
    # if project.visibility == Project.PUBLIC:
    #     return True
    #
    # # check if user if part of center
    # if Center.is_user_part_of_center(project.center, request.user):
    #     return True
    #
    # if Center.is_center_part_of_same_group(project.center, request.user.center):
    #     return True

    return True

def can_publish(project, request):
    if project.center != None and project.center != request.user.center:
        return False
    return True

def my_custom_boolean_filter(value):
    return True

register.filter('can_edit', can_edit)
register.filter('can_view', can_view)
register.filter('can_publish', can_publish)
register.filter('my_custom_boolean_filter', my_custom_boolean_filter)
