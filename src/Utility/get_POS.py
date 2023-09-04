import re
from pathlib import Path

from botok import WordTokenizer
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
            if curr_node_sense.get("freq", 0) == 0 and max_freq == -1:
                max_freq = 1
                word_pos = curr_node_sense["pos"]
                continue
            if curr_node_sense.get("freq", 0) == 0:
                continue
            if curr_node_sense["freq"] > max_freq:
                max_freq = curr_node_sense["freq"]
                word_pos = curr_node_sense["pos"]

        return word_pos

    return NO_POS


def get_POS_through_Word_Tokenizer(string):
    config = Config(dialect_name="general", base_path=Path.home())
    wt = WordTokenizer(config=config)
    token_list = wt.tokenize(string, split_affixes=False)
    if len(token_list) == 1:
        token = token_list[0]
        token_senses = token["senses"]
        unique_token_senses = list(set(token_senses))
        token_lemma_POS = get_POS(token["lemma"])

        filtered_token_senses = [
            x for x in unique_token_senses if x["pos"] != token_lemma_POS
        ]

        max_freq = -1
        word_pos = ""
        for curr_token_sense in filtered_token_senses:
            if curr_token_sense.get("freq", 0) == 0 and max_freq == -1:
                max_freq = 1
                word_pos = curr_token_sense["pos"]
                continue
            if curr_token_sense.get("freq", 0) == 0:
                continue
            if curr_token_sense["freq"] > max_freq:
                max_freq = curr_token_sense["freq"]
                word_pos = curr_token_sense["pos"]
        return word_pos
    return get_POS("string")


if __name__ == "__main__":
    word_pos = get_POS("ཆོས་")
    print(word_pos)

    word_pos = get_POS("ཆོ་")
    print(word_pos)
    word_pos = get_POS_through_Word_Tokenizer("ཆོས་")
    word_pos = get_POS_through_Word_Tokenizer("ཆོ་")

    # print(word_pos)
