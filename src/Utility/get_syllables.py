import re
from typing import List

from botok import TSEK


def filter_multiple_tsek(text: str) -> str:
    # Replace multiple consecutive TSEK characters with a single TSEK
    text = re.sub(r"་+", "་", text)
    return text


def get_syllables(text: str) -> List[str]:
    text_to_split = filter_multiple_tsek(text)
    tsek_split_text = re.split(TSEK, text_to_split)

    text_syllables = [syl + TSEK for syl in tsek_split_text[:-1] if syl != ""]
    if tsek_split_text[-1] != "":
        text_syllables.append(tsek_split_text[-1])
    return text_syllables


def get_syllables_without_tsek(text: str) -> List[str]:
    text = filter_multiple_tsek(text)
    text_syllables = re.split(TSEK, text)
    text_syllables = list(filter(None, text_syllables))
    return text_syllables


if __name__ == "__main__":
    print(get_syllables("ལས་པ་"))
