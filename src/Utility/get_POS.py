import re
from pathlib import Path

from botok.config import Config
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
    config = Config(dialect_name="general", base_path=Path.home())
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
        max_freq = -1
        word_pos = ""
        for curr_node_sense in current_node.data["senses"]:
            if not curr_node_sense["freq"] and max_freq == -1:
                max_freq = 1
                word_pos = curr_node_sense["pos"]
                continue
            if curr_node_sense["freq"] > max_freq:
                max_freq = curr_node_sense["freq"]
                word_pos = curr_node_sense["pos"]

        return word_pos

    return NO_POS


if __name__ == "__main__":
    word_pos = get_POS("ཆོས་")
    print(word_pos)
