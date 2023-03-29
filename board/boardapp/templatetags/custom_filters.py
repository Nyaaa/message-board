from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    _dict = context['request'].GET.copy()
    for key, value in kwargs.items():
        _dict[key] = value
    return _dict.urlencode()
