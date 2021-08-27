import re

replace_dictionary = {
    "lead_double": {"text": u"\u201c", "replace": '"'},
    "follow_double": {"text": u"\u201d", "replace": '"'},
    "lead_single": {"text": u"\u2018", "replace": "'"},
    "follow_single": {"text": u"\u2019", "replace": "'"},
}


def fix_text(inText: str) -> str:
    outText = inText
    for item in replace_dictionary:
        outText = re.sub(item["text"], item["replace"], outText)
    return outText


# This doesn't work...
a = "the �City�) and the former Redevelopment Agency of "

re.sub(
    replace_dictionary["lead_double"]["text"],
    replace_dictionary["lead_double"]["replace"],
    a,
)
