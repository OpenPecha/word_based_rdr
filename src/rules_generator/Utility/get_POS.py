from pathlib import Path

from botok import WordTokenizer
from botok.config import Config
from botok.textunits.bosyl import BoSyl
from botok.tries.trie import Trie

from .get_syllables import get_syllables_without_tsek

TSEK = "་"
NO_POS = "NO_POS"


def get_word_senses(word_string):
    config = Config(dialect_name="general", base_path=Path.home())
    trie = Trie(
        BoSyl,
        profile=config.profile,
        main_data=config.dictionary,
        custom_data=config.adjustments,
    )
    syls = get_syllables_without_tsek(word_string)
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
        return current_node.data["senses"]
    return []


def get_POS(word_string, is_first_iteration=True):
    # First we try to find the POS from botok Word Tokenizer, (Tries to eliminate senses of lemma and returns it)
    POS_from_Word_Tokenizer = get_POS_through_Word_Tokenizer(
        word_string, is_first_iteration
    )
    if POS_from_Word_Tokenizer:
        return POS_from_Word_Tokenizer

    # If we are not able to find POS from above method,
    # Then we select the sense with most freq,
    config = Config(dialect_name="general", base_path=Path.home())
    trie = Trie(
        BoSyl,
        profile=config.profile,
        main_data=config.dictionary,
        custom_data=config.adjustments,
    )
    syls = get_syllables_without_tsek(word_string)
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


def remove_duplicates_list_of_dicts(list_of_dicts):
    seen_tuples = set()
    unique_list = []

    for d in list_of_dicts:
        d_tuple = tuple(sorted(d.items()))
        if d_tuple not in seen_tuples:
            unique_list.append(d)
            seen_tuples.add(d_tuple)

    return unique_list


def get_POS_through_Word_Tokenizer(string, is_first_iteration=True):
    config = Config(dialect_name="general", base_path=Path.home())
    wt = WordTokenizer(config=config)
    token_list = wt.tokenize(string, split_affixes=False)
    # After the tokenizer, if this is still a word, we will try to get POS from this data
    if len(token_list) == 1:
        token = token_list[0]
        token_senses = token["senses"]
        # In some cases, there are 3 senses given, 2 are duplication of each other
        # EG: the word ཆོས་
        unique_token_senses = remove_duplicates_list_of_dicts(token_senses)
        if len(unique_token_senses) == 1:
            return unique_token_senses[0]["pos"]

        if not is_first_iteration:
            return ""
        # If there are more than one sense for a word, sometimes the sense of lemma is included in the sense
        # EG: the word ཆོས་ , there are 3 senses (given 2 are duplicates), the first sense is of lemma ཆོ་
        # pos: OTHER, freq: 322, affixed: True, lemma: ཆོ་
        # pos: NOUN, freq: 392115, affixed: False,  lemma: ཆོ་
        # pos: NOUN, freq: 392115, affixed: False, lemma: ཆོ་
        token_lemma_POS = get_POS(token["lemma"], False)

        # Removing the sense of lemma
        filtered_token_senses = [
            x for x in unique_token_senses if x["pos"] != token_lemma_POS
        ]

        # if there are still more senses left, one with most 'freq' (frequency) is returned
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
    return False


if __name__ == "__main__":
    # word_pos = get_POS_through_Word_Tokenizer("ཆོས་")
    word_pos = get_POS("ལས་")
    print(word_pos)
    print(get_word_senses("ལས་"))
