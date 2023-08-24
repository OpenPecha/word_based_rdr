import re

from botok import Config
from botok.textunits.bosyl import BoSyl
from botok.tries.trie import Trie

TSEK = "་"
NO_POS = "NO_POS"


def split_by_TSEK_without_TsekConcat(word_string):
    pattern = r"[་]+"
    replacement = "་"
    # Removing multiple TSEKs to one just one TSEK
    word_string = re.sub(pattern, replacement, word_string)
    split_pattern = TSEK
    # Spliting the string with TSEK
    word_tsek_splited_list = re.split(split_pattern, word_string)
    word_tsek_splited_list = list(filter(None, word_tsek_splited_list))
    return word_tsek_splited_list


def get_POS(word_string):
    config = Config()
    trie = Trie(
        BoSyl,
        profile=config.profile,
        main_data=config.dictionary,
        custom_data=config.adjustments,
    )
    syls = split_by_TSEK_without_TsekConcat(word_string)
    current_node = None
    for i in range(len(syls)):
        syl = syls[i]
        current_node = trie.walk(syl, current_node)

    # Getting POS from all the data from current node
    if (
        current_node is not None
        and "senses" in current_node.data
        and current_node.data["senses"]
    ):
        word_pos = current_node.data["senses"][0]["pos"]
        return word_pos

    return NO_POS


if __name__ == "__main__":
    word_pos = get_POS("ལ་ལ་")
    print(word_pos)
