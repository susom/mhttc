from django import template
register = template.Library()
import time, datetime
def can_edit(project, request):
    # check if user if part of center
    if request.path == '/projects/search/':
        return False
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

def convert_to_timestampt(date, request):
    return time.mktime(datetime.datetime.strptime(date, "%B %j, %Y").timetuple())

register.filter('convert_to_timestampt', convert_to_timestampt)
register.filter('can_edit', can_edit)
register.filter('can_view', can_view)
register.filter('can_publish', can_publish)
