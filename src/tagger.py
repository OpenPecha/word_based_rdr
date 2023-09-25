from pathlib import Path
from typing import List

from botok import TSEK

from .compare_strings import compare_gold_corpus_and_tokenized_output
from .data_processor import remove_extra_spaces
from .Utility.get_syllables import get_syllables


def split_words_into_syllables(words_list: List[str]) -> List[str]:
    syllables = []

    for words in words_list:
        if TSEK in words:
            tsek_split_words = words.split(TSEK)
            syllables += tsek_split_words
        else:
            syllables.append(words)
    syllables = list(filter(None, syllables))
    return syllables


# Building a tagged list for unmatched gold corpus syllables
def gold_corpus_tagger(gold_corpus_words, gold_index, gold_index_track):
    """
    Input: List of words of gold corpus
    Output: list of each syllable followed by the proper tag
    Eg:
    Input: ['ལ་', 'ལ་ལ་', 'ལ་', 'ལ་བ་'], gold_index=0, gold_index_track =3
    Output: ['ལ་', 'B', 'ལ་','B', 'ལ་', 'I', 'ལ་','B']

    B: means start of new word
    I: Continuation of the previous word
    X: New word but contains affix in gold corpus i.e ར|ས|འི|འམ|འང|འོ|འིའོ|འིའམ|འིའང|འོའམ|འོའང
    Y: Continuation of the previous word but contains affix
    """
    gold_corpus_unmatched_word_list = gold_corpus_words[gold_index:gold_index_track]
    gold_corpus_syls_tagged = []

    for gold_corpus_unmatched_word in gold_corpus_unmatched_word_list:

        gold_corpus_unmatched_syls = get_syllables(gold_corpus_unmatched_word)

        new_word = True
        for gold_corpus_unmatched_syl in gold_corpus_unmatched_syls:
            gold_corpus_syls_tagged.append(gold_corpus_unmatched_syl)
            if new_word:
                if "-" in gold_corpus_unmatched_syl:
                    gold_corpus_syls_tagged.append("X")
                else:
                    gold_corpus_syls_tagged.append("B")
                new_word = False
            else:
                if "-" in gold_corpus_unmatched_syl:
                    gold_corpus_syls_tagged.append("Y")
                else:
                    gold_corpus_syls_tagged.append("I")
    return gold_corpus_syls_tagged


def tagger(gold_corpus):

    (
        is_syllables_separated_correctly,
        gold_corpus_output,
        tokenized_output,
    ) = compare_gold_corpus_and_tokenized_output(gold_corpus)

    if is_syllables_separated_correctly is False:
        return "Error tagger.py: Output of gold corpus and tokenized output does not match. "

    gold_corpus_output = remove_extra_spaces(gold_corpus_output)
    tokenized_output = remove_extra_spaces(tokenized_output)

    gold_corpus_words = gold_corpus_output.split()

    botok_words = tokenized_output.split()
    botok_words_count = len(botok_words)
    gold_corpus_words_count = len(gold_corpus_words)

    gold_index = 0
    botok_index = 0
    tagged_content = ""
    while botok_index < botok_words_count and gold_index < gold_corpus_words_count:
        # Checking if the word is same, '_' is ignored because of possiblity of shads alignment
        condition1 = botok_words[botok_index].replace("_", "") == gold_corpus_words[
            gold_index
        ].replace("_", "")

        # If the word matches perfectly in output of both botok and gold corpus
        if condition1:
            tagged_content += botok_words[botok_index] + "/U "
            gold_index += 1
            botok_index += 1
            continue

        gold_index_track = gold_index
        botok_index_track = botok_index

        # Find the occurence of the next perfect word that matches in output of both botok and gold corpus
        while (botok_index_track < botok_words_count) and (
            gold_index_track < gold_corpus_words_count
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

            botok_unmatched_words = botok_unmatched_words.replace("_", "").replace(
                "-", ""
            )
            gold_corpus_unmatched_words = gold_corpus_unmatched_words.replace(
                "_", ""
            ).replace("-", "")

            if condition_1 and (
                len(botok_unmatched_words) == len(gold_corpus_unmatched_words)
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

        # Calling function to get a tagged list for unmatched gold corpus syllables
        gold_corpus_syls_tagged = gold_corpus_tagger(
            gold_corpus_words, gold_index, gold_index_track
        )

        # Building tagged list for unmatched max match words based on gold corpus syllables
        botok_unmatched_word_list = botok_words[botok_index:botok_index_track]

        gold_corpus_syls_tagged_index = 0
        for botok_unmatched_word in botok_unmatched_word_list:
            botok_unmatched_syls = get_syllables(botok_unmatched_word)
            botok_unmatched_syls_count = len(botok_unmatched_syls)
            botok_syls = ""
            botok_tags = ""

            botok_unmatched_syls_index = 0
            for i in range(
                gold_corpus_syls_tagged_index,
                (gold_corpus_syls_tagged_index + (2 * botok_unmatched_syls_count)),
                2,
            ):
                # botok_syls += gold_corpus_syls_tagged[i]
                botok_syls += botok_unmatched_syls[botok_unmatched_syls_index]
                botok_unmatched_syls_index += 1
                botok_tags += gold_corpus_syls_tagged[i + 1]

            tagged_content += botok_syls + "/" + botok_tags + " "
            gold_corpus_syls_tagged_index = gold_corpus_syls_tagged_index + (
                2 * botok_unmatched_syls_count
            )

        gold_index = gold_index_track
        botok_index = botok_index_track

    return tagged_content


if __name__ == "__main__":
    file_string = Path("src/data/TIB_train.txt").read_text(encoding="utf-8")
    tagged_output = tagger(file_string)
    with open("src/data/TIB_tagged.txt", "w", encoding="utf-8") as file:
        file.write(tagged_output)
