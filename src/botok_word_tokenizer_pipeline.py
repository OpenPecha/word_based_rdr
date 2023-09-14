from botok import Text

from .data_processor import (  # noqa
    remove_extra_spaces,
    transform_gold_corpus_for_botok_word_tokenizer_pipeline,
)
from .Utility.regex_replacer import replace_with_regex  # noqa


def botok_word_tokenizer_pipeline(file_string):
    """
    input: string of a file before going under max match(botok)
    output/return: cleaned/preprocess string and word segmented
    """
    preprocessed_string = transform_gold_corpus_for_botok_word_tokenizer_pipeline(
        file_string
    )
    t = Text(preprocessed_string)
    max_match_output = t.tokenize_words_raw_text
    max_match_output = remove_extra_spaces(max_match_output)
    """
    Input: རིན་པོ་ཆེའི་, max match output: རིན་པོ་ཆེ འི་, after replacement རིན་པོ་ཆེ-འི་
    """
    pattern = r"((?![་།_༠༡༢༣༤༥༦༧༨༩])[\u0F00-\u0FFF]) (ར|ས|འི|འམ|འང|འོ|འིའོ|འིའམ|འིའང|འོའམ|འོའང)"
    replacement = r"\1-\2"
    max_match_output = replace_with_regex({pattern: replacement}, max_match_output)
    return max_match_output


if __name__ == "__main__":
    word = "༄༅། །རྒྱལ་པོ་ ལ་ གཏམ་ བྱ་བ་ རིན་པོ་ཆེ འི་ ཕྲེང་་་བ། ལ་ ལ་ལ་ ལ་ ལ་བ་ ཡོད། དཔལ། དགེའོ་ བཀྲ་ཤིས་ ཤོག།"
    botok_output = botok_word_tokenizer_pipeline(word)
    print(botok_output)
