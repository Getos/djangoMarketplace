# your_app/templatetags/custom_tags.py

from django import template

register = template.Library()


@register.simple_tag
def user_in_groups(user, *group_names):
    return user.is_authenticated and any(user.groups.filter(name=group).exists() for group in group_names)
