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


@register.filter(name="start_index")
def start_index(value, start):
    return value[start:]


@register.filter(name="end_index")
def end_index(value, end):
    return value[:end]