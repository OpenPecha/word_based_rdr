from botok import Text 

from ..preprocessing.preprocessor import replace_initial_patterns
from ..preprocessing.preprocessor import file_2_botok

def botok_max_matcher(file_string):
    """
    input: string of a file before going under max match(botok)
    output/return: cleaned/preprocess string and word segmented
    """
    preprocessed_string = file_2_botok(file_string)
    t = Text(preprocessed_string)
    max_match_output = t.tokenize_words_raw_text
    return max_match_output


if __name__ == "__main__":
    pass
