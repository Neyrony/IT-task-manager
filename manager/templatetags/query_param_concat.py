from django import template
from django.http import HttpRequest

register = template.Library()


@register.simple_tag
def query_param_concat(request: HttpRequest, **kwargs) -> str:
    update = request.GET.copy()

    for key, value in kwargs.items():
        if value is not None:
            update[key] = value
        else:
            update.pop(key, None)

    return update.urlencode()
