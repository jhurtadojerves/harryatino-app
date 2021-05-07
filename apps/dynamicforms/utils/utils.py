from .regex import split_regex_text, get_match_regex


def items_attr(attrs):
    items = {}
    if attrs:
        items_widget = split_regex_text(attrs, "[;\n\r]+")
        for item in items_widget:
            key, value = get_match_regex(item)
            items.update({key: value})
    return items


def get_type_and_widget(field):
    try:
        _type, _widget = field.split(":")
    except ValueError:
        _type, _widget = field, None
    return _type, _widget
