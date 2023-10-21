from django import template

register = template.Library()

@register.filter
def get_item_at_index(lst, index):
    return lst[index]
