import re
from typing import List

from botok import TSEK


def filter_multiple_tsek(text: str) -> str:
    pattern = r"[་]+"  # Removing multiple TSEKs
    replacement = "་"
    text = re.sub(pattern, replacement, text)
    return text


def get_syllables(text: str) -> List[str]:
    text_to_split = filter_multiple_tsek(text)
    text_syllables = re.split(TSEK, text_to_split)
    if len(text_syllables) == 1:
        return text_syllables
    for index, element in enumerate(text_syllables):
        if element == "":
            text_syllables[index - 1] += TSEK
            break
        if index == len(text_syllables) - 1:
            break
        if text_syllables[index + 1] != "":
            text_syllables[index] += TSEK

    text_syllables = list(filter(None, text_syllables))
    return text_syllables


def get_syllables_without_tsek(text: str) -> List[str]:
    text = filter_multiple_tsek(text)
    text_syllables = re.split(TSEK, text)
    text_syllables = list(filter(None, text_syllables))
    return text_syllables


if __name__ == "__main__":
    print(get_syllables("ལ-ས་པ་"))
