from pathlib import Path
from django import template

register = template.Library()


@register.filter
def basename(value: str) -> str:
    """file/path/to/name.xlsx → name.xlsx"""
    return Path(value).name
