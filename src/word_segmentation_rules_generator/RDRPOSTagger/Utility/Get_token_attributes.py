from pathlib import Path

from botok import WordTokenizer
from botok.config import Config


def Get_CONTENT_POS_attributes(string_text):
    content_list = []
    pos_list = []
    tokens = Tokenize_words(string_text)
    for token in tokens:
        content_list.append(token.text)
        pos_list.append(token.pos)
    return content_list, pos_list


def Tokenize_words(string_text):
    config = Config(dialect_name="general", base_path=Path.home())
    wt = WordTokenizer(config=config)
    tokens = wt.tokenize(string_text, split_affixes=False, spaces_as_punct=False)
    return tokens
