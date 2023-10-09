from django import template

register = template.Library()

@register.filter(name='get_by_row_and_number')
def get_by_row_and_number(queryset, row, number):
    # Your filter logic here
    ...
