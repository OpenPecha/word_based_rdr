import re
from pathlib import Path

from botok import WordTokenizer
from botok.config import Config

from rules_generator.data_processor import prepare_gold_corpus_for_tokenizer


def Get_CONTENT_POS_attributes(string_text):

    # This is done so that we could tokenize properly and getting proper POS list
    # With word like བོད་པ-འི་, we need POS of whole word, but in WordTokenizer,
    # This would be three tokens བོད་པ, -, འི་ and returns three POS which we dont need
    # So  we convert  བོད་པ-འི་ ->བོད་པའི་ and get only one POS
    pattern = r"([^ ])-([^ ])"
    replacement = r"\1\2"
    string_text = re.sub(pattern, replacement, string_text)
    string_text = prepare_gold_corpus_for_tokenizer(string_text)
    tokens = Tokenize_words(string_text)

    pos_list = []

    for token in tokens:
        pos_list.append(token.pos)
    return pos_list


def Tokenize_words(string_text):
    config = Config(dialect_name="general", base_path=Path.home())
    wt = WordTokenizer(config=config)
    tokens = wt.tokenize(string_text, split_affixes=False, spaces_as_punct=False)
    return tokens
