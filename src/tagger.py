from pathlib import Path
from typing import List

from botok import TSEK

from .compare_strings import compare_gold_corpus_and_tokenized_output
from .data_processor import remove_extra_spaces
from .Utility.get_syllables import get_syllables


def split_words_into_syllables(words_list: List[str]) -> List[str]:
    syllables = []

    for word in words_list:
        if TSEK in word:
            tsek_split_words = word.split(TSEK)
            syllables += tsek_split_words
        else:
            syllables.append(word)

    # Remove empty entries
    syllables = list(filter(None, syllables))
    return syllables


def tag_syllables(syllable_list: List[str]) -> List[str]:
    """
    Args:
        syllable_list (list of str): List of words from the gold corpus.
    Returns:
        list of str: List of syllables with proper tags.
    """
    tagged_syllables = []

    for word in syllable_list:
        syllables = get_syllables(word)
        new_word = True

        for syl in syllables:
            tagged_syllables.append(syl)

            if new_word:
                tag = "B" if "-" not in syl else "X"
                new_word = False
            else:
                tag = "I" if "-" not in syl else "Y"
            tagged_syllables.append(tag)

    return tagged_syllables


def find_next_matching_words(botok_words, gold_corpus_words, botok_index, gold_index):
    """
    Find the next matching words between botok and gold corpus starting from given indices.
    Returns the indices of the last matching words found.
    """
    gold_index_track, botok_index_track = gold_index, botok_index

    while botok_index_track < len(botok_words) and gold_index_track < len(
        gold_corpus_words
    ):
        condition_1 = botok_words[botok_index_track].replace(
            "_", ""
        ) == gold_corpus_words[gold_index_track].replace("_", "")

        botok_unmatched_words = "".join(
            botok_words[botok_index : botok_index_track + 1]  # noqa
        )
        gold_corpus_unmatched_words = "".join(
            gold_corpus_words[gold_index : gold_index_track + 1]  # noqa
        )

        botok_unmatched_words = botok_unmatched_words.replace("_", "").replace("-", "")
        gold_corpus_unmatched_words = gold_corpus_unmatched_words.replace(
            "_", ""
        ).replace("-", "")

        if condition_1 and len(botok_unmatched_words) == len(
            gold_corpus_unmatched_words
        ):
            break

        botok_unmatched_syls = split_words_into_syllables(
            botok_words[botok_index : botok_index_track + 1]  # noqa
        )
        gold_corpus_unmatched_syls = split_words_into_syllables(
            gold_corpus_words[gold_index : gold_index_track + 1]  # noqa
        )

        if len(botok_unmatched_syls) > len(gold_corpus_unmatched_syls):
            gold_index_track += 1
        elif len(botok_unmatched_syls) < len(gold_corpus_unmatched_syls):
            botok_index_track += 1
        else:
            gold_index_track += 1
            botok_index_track += 1

    return gold_index_track, botok_index_track


def tag_unmatched_words(botok_words, gold_corpus_words, botok_index, gold_index):
    """
    Tag unmatched words based on gold corpus syllables and return the tagged content.
    Returns the tagged content and the indices after tagging.
    """
    gold_index_track, botok_index_track = find_next_matching_words(
        botok_words, gold_corpus_words, botok_index, gold_index
    )

    gold_corpus_syls_tagged = tag_syllables(
        gold_corpus_words[gold_index:gold_index_track]
    )

    botok_unmatched_word_list = botok_words[botok_index:botok_index_track]

    gold_corpus_syls_tagged_index = 0
    tagged_content = ""

    for botok_unmatched_word in botok_unmatched_word_list:
        botok_unmatched_syls = get_syllables(botok_unmatched_word)
        botok_unmatched_syls_count = len(botok_unmatched_syls)
        botok_syls = ""
        botok_tags = ""

        botok_unmatched_syls_index = 0

        for i in range(
            gold_corpus_syls_tagged_index,
            gold_corpus_syls_tagged_index + (2 * botok_unmatched_syls_count),
            2,
        ):
            botok_syls += botok_unmatched_syls[botok_unmatched_syls_index]
            botok_unmatched_syls_index += 1
            botok_tags += gold_corpus_syls_tagged[i + 1]

        tagged_content += botok_syls + "/" + botok_tags + " "
        gold_corpus_syls_tagged_index = gold_corpus_syls_tagged_index + (
            2 * botok_unmatched_syls_count
        )

    return tagged_content, gold_index_track, botok_index_track


def tagger(gold_corpus):
    # Compare gold_corpus and tokenized_output
    (
        is_syllables_separated_correctly,
        gold_corpus_output,
        tokenized_output,
    ) = compare_gold_corpus_and_tokenized_output(gold_corpus)

    if not is_syllables_separated_correctly:
        return "Error tagger.py: Output of gold corpus and tokenized output does not match."

    gold_corpus_output = remove_extra_spaces(gold_corpus_output)
    tokenized_output = remove_extra_spaces(tokenized_output)

    gold_corpus_words = gold_corpus_output.split()
    botok_words = tokenized_output.split()

    gold_index, botok_index = 0, 0
    tagged_content = ""

    while botok_index < len(botok_words) and gold_index < len(gold_corpus_words):
        # Checking if the word is the same (ignoring '_' due to possible shads alignment)
        condition1 = botok_words[botok_index].replace("_", "") == gold_corpus_words[
            gold_index
        ].replace("_", "")

        # If the word matches perfectly in output of both botok and gold corpus
        if condition1:
            tagged_content += botok_words[botok_index] + "/U "
            gold_index += 1
            botok_index += 1
            continue

        unmatched_tagged_content, gold_index, botok_index = tag_unmatched_words(
            botok_words, gold_corpus_words, botok_index, gold_index
        )
        tagged_content += unmatched_tagged_content

    return tagged_content


if __name__ == "__main__":
    file_string = Path("src/data/TIB_train.txt").read_text(encoding="utf-8")
    tagged_output = tagger(file_string)
    with open("src/data/TIB_tagged.txt", "w", encoding="utf-8") as file:
        file.write(tagged_output)
