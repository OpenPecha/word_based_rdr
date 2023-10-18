from botok.tokenizers import WordTokenizer

from rules_generator.data_processor import (
    prepare_gold_corpus_for_tokenizer,
    remove_extra_spaces,
)
from rules_generator.Utility.regex_replacer import replace_with_regex


def botok_word_tokenizer_pipeline(gold_corpus: str) -> str:
    """
    input: string of a file before going under max match(botok)
    output/return: cleaned/preprocess string and word segmented
    """
    preprocessed_text = prepare_gold_corpus_for_tokenizer(gold_corpus)
    wt = WordTokenizer()
    tokenized_tokens = wt.tokenize(preprocessed_text)
    tokenized_text = " ".join(
        tokenized_token.text for tokenized_token in tokenized_tokens
    )
    tokenized_text = remove_extra_spaces(tokenized_text)
    tokenized_text = add_hyphens_to_affixes(tokenized_text)
    return tokenized_text


def add_hyphens_to_affixes(text: str) -> str:
    """
    Input: རིན་པོ་ཆེའི་, tokenized output: རིན་པོ་ཆེ འི་, after replacement རིན་པོ་ཆེ-འི་
    """
    pattern = r"((?![་།_༠༡༢༣༤༥༦༧༨༩])[\u0F00-\u0FFF]) (ར|ས|འི|འམ|འང|འོ|འིའོ|འིའམ|འིའང|འོའམ|འོའང)"
    replacement = r"\1-\2"
    text = replace_with_regex({pattern: replacement}, text)
    return text


if __name__ == "__main__":
    word = "༄༅། །རྒྱལ་པོ་ ལ་ གཏམ་ བྱ་བ་ རིན་པོ་ཆེ འི་ ཕྲེང་་་བ། ལ་ ལ་ལ་ ལ་ ལ་བ་ ཡོད། དཔལ། དགེའོ་ བཀྲ་ཤིས་ ཤོག།"
    botok_output = botok_word_tokenizer_pipeline(word)
    print(botok_output)
