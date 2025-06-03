from django import template

register = template.Library()


@register.filter(name='seconds_to_minutes')
def seconds_to_minutes(seconds):
    """Convert seconds to minutes."""
    minutes = seconds // 60
    return f"{minutes} min" if minutes > 0 else "< 1 min"
