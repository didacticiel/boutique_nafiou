# store/templatetags/custom_filters.py

from django import template

register = template.Library()

@register.filter
def range_filter(value):
    return range(value)

@register.filter
def get_item(dictionary, key):
    """Récupère une valeur par clé dans un dictionnaire."""
    return dictionary.get(str(key), 0)



# @register.filter
# def get_item(dictionary, key):
#     return dictionary.get(str(key))
