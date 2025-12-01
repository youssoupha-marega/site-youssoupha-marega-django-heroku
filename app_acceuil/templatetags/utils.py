from django import template

register = template.Library()


@register.filter(name='prefix')
def prefix(value):
    """
    Extract the prefix (first part before underscore) from a URL name.
    For example: 'blogue_list' -> 'blogue', 'projet_detail' -> 'projet'
    """
    if value:
        return value.split('_')[0]
    return value
