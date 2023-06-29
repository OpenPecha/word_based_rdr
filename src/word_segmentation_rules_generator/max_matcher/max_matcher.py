import re

from botok import Text

from ..preprocessing.preprocessor import adjust_spaces, file_2_botok


def botok_max_matcher(file_string):
    """
    input: string of a file before going under max match(botok)
    output/return: cleaned/preprocess string and word segmented
    """
    preprocessed_string = file_2_botok(file_string)
    t = Text(preprocessed_string)
    max_match_output = t.tokenize_words_raw_text
    max_match_output = adjust_spaces(max_match_output)
    """
    Input: རིན་པོ་ཆེའི་, max match output: རིན་པོ་ཆེ འི་, after replacement རིན་པོ་ཆེ-འི་
    """
    pattern = r"((?![་།_༠༡༢༣༤༥༦༧༨༩])[\u0F00-\u0FFF]) (ར|ས|འི|འམ|འང|འོ|འིའོ|འིའམ|འིའང|འོའམ|འོའང)"

    replacement = r"\1-\2"
    max_match_output = re.sub(pattern, replacement, max_match_output)
    return max_match_output


if __name__ == "__main__":
    pass
