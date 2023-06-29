import re

from botok import TSEK


def replace_initial_patterns(file_string, is_gold_corpus=False):
    # Some signs(i.e ?,+,- ) are presented in human annotated training files which needs to be edited
    # There are two different kind of TSEK, and here proper tsek been replaced
    initial_patterns = {"?": " ", "+": "", "-": "", "༌": TSEK}
    if is_gold_corpus:
        initial_patterns = {"?": " ", "+": "", "༌": TSEK}

    modified_content = re.sub(
        "|".join(re.escape(key) for key in initial_patterns.keys()),
        lambda match: initial_patterns[match.group(0)],
        file_string,
    )
    modified_content = adjust_spaces(modified_content)
    return modified_content


def adjust_spaces(file_string):
    pattern = r"[ ]+"
    replacement = " "
    modified_string = re.sub(pattern, replacement, file_string.strip())
    return modified_string


def adjust_spaces_for_non_affix(file_string):
    """
    Sometimes there error in gold corpus i.e
    string: ད གེ འོ་ བཀྲ་ཤིས་ ཤོག།
    Expected: དགེ འོ་ བཀྲ་ཤིས་ ཤོག།
    *Note that in དགེ འོ་, space before འོ་ is not closed,because this is an affix
    """
    pattern = r"([^་།_]) ([^ར ས འི འམ འང འོ འིའོ འིའམ འིའང འོའམ འོའང ། _])"
    replacement = r"\1\2"
    modified_string = re.sub(pattern, replacement, file_string)
    return modified_string


def adjust_spaces_for_affix(file_string):
    """
    Somtimes there error in gold corpus i.e
    String: །འཁོར་བ འི་ འབྲོག་ ནི་ མི་ བཟད་པ-འི།
    Expected string: །འཁོར་བ-འི་ འབྲོག་ ནི་ མི་ བཟད་པ-འི།
    """
    pattern = r"((?![་།_༠༡༢༣༤༥༦༧༨༩])[\u0F00-\u0FFF]) (ར|ས|འི|འམ|འང|འོ|འིའོ|འིའམ|འིའང|འོའམ|འོའང)"
    replacement = r"\1-\2"
    modified_string = re.sub(pattern, replacement, file_string)
    return modified_string


def adjust_spaces_for_tibetan_numbers(file_string):
    modified_content = file_string
    patterns = {
        r"(?<=[༠༡༢༣༤༥༦༧༨༩])([ ]+)(?=[༠༡༢༣༤༥༦༧༨༩])": r"",  # གཏམ་༡ ༢  ༣བྱ་བ་ -> གཏམ་༡༢༣བྱ་བ་
        r"\s*([༠༡༢༣༤༥༦༧༨༩]+)\s*": r" \1 ",  # གཏམ་༡༢༣བྱ་བ་ -> གཏམ་ ༡༢༣ བྱ་བ་,
    }
    for pattern, replacement in patterns.items():
        modified_content = re.sub(pattern, replacement, modified_content)
    return modified_content


def adjust_spaces_for_non_tibetan_character(file_string):
    modified_content = file_string
    patterns = {
        r"(?<=[^\u0F00-\u0FFF\s]) (?=[^\u0F00-\u0FFF\s])": r"",  # For non tibetan characters
        r"\s*([^\u0F00-\u0FFF\s_-]+)\s*": r" \1 ",
    }
    for pattern, replacement in patterns.items():
        modified_content = re.sub(pattern, replacement, modified_content)
    return modified_content


def file_2_botok(file_string):
    """
    input: string of a file before going under max match(botok)
    output/return: cleaned/preprocess string
    """

    modified_content = replace_initial_patterns(file_string)

    # Joining all the words, not leaving spaces unless its for SHAD
    patterns = {r"(?<=([^།])) (?=([^།]))": ""}

    for pattern, replacement in patterns.items():
        modified_content = re.sub(pattern, replacement, modified_content)
    return modified_content


def gold_corpus_2_tagger(file_string):
    """
    input: string where words are separated with space by human annotators before going to tagger
    output/return: cleaned/preprocess string where words are still separated by space
    """
    modified_content = replace_initial_patterns(file_string, is_gold_corpus=True)

    patterns = {
        "།[ ]+༄": "།_༄",  # ཕྲེང་བ།  ༄༅༅།-> ཕྲེང་བ།_༄༅༅།
        "༅[ ]+།": "༅_།",
        "(?<=།) (?=།)": "_",  # ༄༅༅། ། ། །རྒྱ་གར་ སྐད་དུ། -> ༄༅༅།_།_།_།རྒྱ་གར་ སྐད་དུ།
        "[ ]+།": "_།",  # རྣམ་གྲོལ་ ཞིང༌ ། ། ->རྣམ་གྲོལ་ ཞིང་ _།_།,
        "།[ ]+": "།_",
        r"(?<![༅།_])([།_]+)": r" \1",  # སྐད་དུ།_རཱ་ -> སྐད་དུ །_རཱ་
        r"([།_]+)(?![༄།_])": r"\1 ",  # སྐད་དུ།_རཱ་ -> སྐད་དུ།_ རཱ་
    }
    for pattern, replacement in patterns.items():
        modified_content = re.sub(pattern, replacement, modified_content)
    gold_corpus_output = adjust_spaces_for_non_affix(modified_content)
    gold_corpus_output = adjust_spaces_for_tibetan_numbers(gold_corpus_output)
    gold_corpus_output = adjust_spaces_for_non_tibetan_character(gold_corpus_output)
    gold_corpus_output = adjust_spaces_for_affix(gold_corpus_output)

    return gold_corpus_output


if __name__ == "__main__":
    pass
