from django import template


register = template.Library()

@register.simple_tag(takes_context=True)
def param_replace(context, **kwargs):
    d = context['request'].GET.copy()

    if 'remove_page' in kwargs:
        if 'page' in d:
            del d['page']
        del kwargs['remove_page']

    for k, v in kwargs.items():
        d[k] = v
    for k in [k for k, v in d.items() if not v]:
        del d[k]

    return d.urlencode()