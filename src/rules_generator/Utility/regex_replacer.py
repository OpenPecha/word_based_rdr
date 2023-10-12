import re
from typing import Dict


def replace_with_regex(patterns_replacements: Dict, text: str) -> str:
    for pattern, replace in patterns_replacements.items():
        text = re.sub(pattern, replace, text)
    return text


if __name__ == "__main__":
    tibetan_text = "བདེ་ལེགས་ཞུ་ཞུ་ཞུ་་་ཞུ"
    patterns_replacements = {
        r"་+": "་",  # Replace multiple consecutive TSEK characters with a single TSEK
        r"ད": "བ",  # Replace 'ད' with 'བ'
    }

    modified_text = replace_with_regex(patterns_replacements, tibetan_text)
    print(modified_text)
