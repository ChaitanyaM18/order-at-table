from django import template

register = template.Library()

@register.filter
def split_filter(value):
    '''
    Divides the value; argument is the divisor.
    Returns empty string on any error.
    '''
    try:
        if value:
            print(type(value))
            return [item for item in value]
    except:
        pass
    return ''
