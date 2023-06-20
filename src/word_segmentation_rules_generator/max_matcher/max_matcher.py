from botok import Text 

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
    t = Text(file_string)
    max_match_output = t.tokenize_words_raw_text
    return max_match_output


if __name__ == "__main__":
    # print(botok_max_matcher("༄༅། །རྒྱལ་པོ་ ལ་ གཏམ་ བྱ་བ་ རིན་པོ་ཆེའི་ ཕྲེང་བ།"), end="")
    pass
