from django import template

register = template.Library()

@register.filter(name='add_class')
def add_class(field, css_class):
    # Check if the field is indeed a form field
    if hasattr(field, 'as_widget'):
        return field.as_widget(attrs={"class": css_class})
    # If not, return the original field without modification
    return field
