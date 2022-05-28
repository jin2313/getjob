from django import template

register = template.Library()


@register.filter(name="split")
def split(value, key):
    return value.split(key)


@register.filter(name="to_int")
def to_int(value):
    return int(value)


@register.filter(name="to_str")
def to_str(value):
    return str(value)


@register.filter(name="zip")
def zip(value1, value2):
    return zip(value1, value2)