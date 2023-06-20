from pathlib import Path

from botok import WordTokenizer
from botok.config import Config

from ..preprocessing.preprocessor import replace_initial_patterns


def botok_max_matcher(file_string):
    """
    input: string of a file before going under max match(botok)
    output/return: cleaned/preprocess string and word segmented
    Eg:>
    Input string :>༄༅། །རྒྱལ་པོ་ ལ་ གཏམ་ བྱ་བ་ རིན་པོ་ཆེ-འི་ ཕྲེང་བ།
    Output string:>  རྒྱལ་པོ་ ལ་ གཏམ་ བྱ་བ་ རིན་པོ་ཆེའི་ ཕྲེང་བ་
    """
    file_string = replace_initial_patterns(file_string)
    config = Config(dialect_name="general", base_path=Path.home())
    wt = WordTokenizer(config=config)
    tokens = wt.tokenize(file_string, split_affixes=False)
    max_match_output = ""
    for token in tokens:
        max_match_output += token.text_cleaned + " "
    return max_match_output


if __name__ == "__main__":
    # print(botok_max_matcher("༄༅། །རྒྱལ་པོ་ ལ་ གཏམ་ བྱ་བ་ རིན་པོ་ཆེའི་ ཕྲེང་བ།"), end="")
    pass
