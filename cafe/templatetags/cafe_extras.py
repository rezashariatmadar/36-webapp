from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """
    Template filter to allow dictionary lookups by key.
    Usage: {{ my_dict|get_item:item_id }}
    """
    if not isinstance(dictionary, dict):
        return 0
    return dictionary.get(str(key), 0)