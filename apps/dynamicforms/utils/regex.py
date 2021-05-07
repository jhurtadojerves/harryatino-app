# Python
import re

ATTRIBUTE_RE = re.compile(
    r"""
    (?P<attr>
        [\w_-]+
    )
    (?P<sign>
        \+?=
    )
    (?P<value>
    [']? # start quote
        [^']*
    [']? # end quote
    )
""",
    re.VERBOSE | re.UNICODE,
)


def get_match_regex(kwargs):
    match = ATTRIBUTE_RE.match(kwargs)
    dct = match.groupdict()
    key, value = dct.get("attr"), dct.get("value")
    return key, value


def split_regex_text(text, split_regex=""):
    return re.split(split_regex, text)
