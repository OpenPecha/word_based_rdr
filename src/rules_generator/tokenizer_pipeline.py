from pathlib import Path

from botok.tokenizers.wordtokenizer import WordTokenizer

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
        tokenized_token.text.strip() for tokenized_token in tokenized_tokens
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
    DATA_DIR = Path(__file__).resolve().parent / "data"
    gold_corpus = Path(DATA_DIR / "gold_corpus.txt").read_text(encoding="utf-8")
    gold_corpus = "༄༅ །། དཔལ་ནག་པོ་ཆེན་པོའི་སྒྲུབ་ཐབས་ཞེས་བྱ་བ། སྒྲུབ་ཐབས་ཀླུ་སྒྲུབ་ཀྱིས་མཛད་པ ༄༅༅༅།། རྒྱ་གར་སྐད་དུ ། "
    tokenized_gold_corpus = botok_word_tokenizer_pipeline(gold_corpus)
    print(tokenized_gold_corpus)
    # with open(DATA_DIR / "gold_corpus_tokenized.txt", "w", encoding="utf-8") as tsvfile:
    #     tsvfile.write(tokenized_gold_corpus)
