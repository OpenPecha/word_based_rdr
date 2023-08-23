import re


def Remove_tag_in_String(string_text):
    patterns_and_replacements = [(r"/[A-Z]+", ""), (r"_", " ")]
    for pattern, replacement in patterns_and_replacements:
        string_text = re.sub(pattern, replacement, string_text)
    return string_text
