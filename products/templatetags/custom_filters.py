from django import template

register = template.Library()

@register.filter
def get_selected_categories(request, category_id):
    selected_categories = request.GET.getlist('category[]')
    return str(category_id) in selected_categories