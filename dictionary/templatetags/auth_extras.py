from django import template

register = template.Library()

@register.simple_tag
def is_authenticated(user):
    """
    Returns True if the user is authenticated, False otherwise.
    """
    return user.is_authenticated

@register.simple_tag
def is_staff(user):
    """
    Returns True if the user is a staff member, False otherwise.
    """
    return user.is_staff

@register.simple_tag
def is_superuser(user):
    """
    Returns True if the user is a superuser, False otherwise.
    """
    return user.is_superuser
