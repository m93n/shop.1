from django import template

register = template.Library()

@register.simple_tag
def divide(first_value, second_value):

    divide_value = int((1 - int(first_value) / int(second_value)) * 100)

    return divide_value