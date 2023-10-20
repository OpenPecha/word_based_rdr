import re
from pathlib import Path

from botok import TSEK

from rules_generator.Utility.regex_replacer import replace_with_regex


def keep_only_tibetan_characters(text: str) -> str:
    return re.sub(r"[^\u0F00-\u0FFF\s\n\t]+", r"", text)


def filter_text(text: str, is_gold_corpus=False) -> str:
    # There are two different kind of TSEK in tibetan, and here standard TSEK is used
    # In gold corpus, i)'-' for affix ii)'+' joiner iii)'?' when annotator is not sure
    # Eg: དགེ-འོ་, ཤེས་རབ་+པོ, རཏྣ་ མཱ་? ལཱི།?
    special_characters = {"?": " ", "+": "", "-": "", "༌": TSEK}
    if is_gold_corpus:
        special_characters = {"?": " ", "+": "", "༌": TSEK}

    text = re.sub(
        "|".join(re.escape(key) for key in special_characters.keys()),
        lambda match: special_characters[match.group(0)],
        text,
    )
    text = remove_extra_spaces(text)
    return text


def remove_extra_spaces(text: str) -> str:
    pattern = r"[ ]+"
    replacement = " "
    text = replace_with_regex({pattern: replacement}, text.strip())
    return text


def adjust_spaces_for_non_affix(text: str) -> str:
    """
    Sometimes there error in gold corpus i.e
    string: ད གེ འོ་ བཀྲ་ཤིས་ ཤོག།
    Expected: དགེ འོ་ བཀྲ་ཤིས་ ཤོག།
    *Note that in དགེ འོ་, space before འོ་ is not closed,because this is an affix
    """
    pattern = r"([^་།_]) ([^ར ས འི འམ འང འོ འིའོ འིའམ འིའང འོའམ འོའང ། _])"
    replacement = r"\1\2"
    text = replace_with_regex({pattern: replacement}, text)
    return text


def adjust_spaces_for_affix(text: str) -> str:
    """
    Somtimes there error in gold corpus i.e
    String: །འཁོར་བ འི་ འབྲོག་ ནི་ མི་ བཟད་པ-འི།
    Expected string: །འཁོར་བ-འི་ འབྲོག་ ནི་ མི་ བཟད་པ-འི།
    """
    pattern = r"((?![་།_༠༡༢༣༤༥༦༧༨༩])[\u0F00-\u0FFF]) (ར|ས|འི|འམ|འང|འོ|འིའོ|འིའམ|འིའང|འོའམ|འོའང)"
    replacement = r"\1-\2"
    text = replace_with_regex({pattern: replacement}, text)

    return text


def adjust_spaces_for_tibetan_numbers(text: str) -> str:
    patterns = {
        r"(?<=[༠༡༢༣༤༥༦༧༨༩])([ ]+)(?=[༠༡༢༣༤༥༦༧༨༩])": r"",  # གཏམ་༡ ༢  ༣བྱ་བ་ -> གཏམ་༡༢༣བྱ་བ་
        r"\s*([༠༡༢༣༤༥༦༧༨༩]+)\s*": r" \1 ",  # གཏམ་༡༢༣བྱ་བ་ -> གཏམ་ ༡༢༣ བྱ་བ་,
    }
    text = replace_with_regex(patterns, text)
    return text


def adjust_spaces_for_non_tibetan_character(text: str) -> str:
    patterns = {
        r"(?<=[^\u0F00-\u0FFF\s]) (?=[^\u0F00-\u0FFF\s])": r"",  # For non tibetan characters
        r"\s*([^\u0F00-\u0FFF\s_-]+)\s*": r" \1 ",
    }
    text = replace_with_regex(patterns, text)
    return text


def add_tsek_before_newline(text):
    # Use regular expression to find newlines without a shad or tsek before them
    pattern = r"([^^་།])(\s*\n)"
    replacement = r"\1་\2"
    return re.sub(pattern, replacement, text)


def prepare_gold_corpus_for_tokenizer(gold_corpus: str) -> str:

    """
    input: string of a file before going under max match(botok)
    output/return: cleaned/preprocess string
    """
    text = add_tsek_before_newline(gold_corpus)
    text = filter_text(text)

    # Joining all the words, not leaving spaces unless its for SHAD
    patterns = {r"(?<=([^།])) (?=([^།]))": ""}

    text = replace_with_regex(patterns, text)
    return text


def transform_gold_corpus_for_tagging(gold_corpus: str) -> str:

    """
    input: string where words are separated with space by human annotators before going to tagger
    output/return: cleaned/preprocess string where words are still separated by space
    """
    text = add_tsek_before_newline(gold_corpus)
    text = filter_text(text, is_gold_corpus=True)

    patterns = {
        "།[ ]+༄": "།_༄",  # ཕྲེང་བ།  ༄༅༅།-> ཕྲེང་བ།_༄༅༅།
        "༅[ ]+།": "༅_།",
        "(?<=།) (?=།)": "_",  # ༄༅༅། ། ། །རྒྱ་གར་ སྐད་དུ། -> ༄༅༅།_།_།_།རྒྱ་གར་ སྐད་དུ།
        "[ ]+།": "_།",  # རྣམ་གྲོལ་ ཞིང༌ ། ། ->རྣམ་གྲོལ་ ཞིང་ _།_།,
        "།[ ]+": "།_",
        r"(?<![༅།_])([།_]+)": r" \1",  # སྐད་དུ།_རཱ་ -> སྐད་དུ །_རཱ་
        r"([།_]+)(?![༄།_])": r"\1 ",  # སྐད་དུ།_རཱ་ -> སྐད་དུ།_ རཱ་
    }
    text = replace_with_regex(patterns, text)
    text = adjust_spaces_for_non_affix(text)
    text = adjust_spaces_for_tibetan_numbers(text)
    text = adjust_spaces_for_non_tibetan_character(text)
    text = adjust_spaces_for_affix(text)

    return text


if __name__ == "__main__":
    DATA_DIR = Path(__file__).resolve().parent / "data"
    gold_corpus = Path(DATA_DIR / "gold_corpus.txt").read_text(encoding="utf-8")
    prepared_gold_corpus = transform_gold_corpus_for_tagging(gold_corpus)
    print(prepared_gold_corpus)
    with open(DATA_DIR / "gold_corpus_prepared.txt", "w", encoding="utf-8") as tsvfile:
        tsvfile.write(prepared_gold_corpus)
