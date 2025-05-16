from django import template

register = template.Library()

@register.filter
def percentage(value, total):
    try:
        value = float(value)
        total = float(total)
        if total == 0:
            return 0
        return round((value / total) * 100, 2)  # برحسب درصد با دو رقم اعشار
    except (ValueError, ZeroDivisionError):
        return 0
