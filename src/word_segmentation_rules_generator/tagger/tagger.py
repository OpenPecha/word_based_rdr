import re

from botok import TSEK

from ..comparator.comparator import comparator


def split_by_TSEK(string_to_split):
    split_pattern = r"[༌་]"
    string_to_split = re.split(split_pattern, string_to_split)
    string_to_split = list(filter(None, string_to_split))
    return string_to_split


# Building a tagged list for unmatched gold corpus syllables
def gold_corpus_tagger(gold_corpus_words, gold_index, gold_index_track):
    """
    Input: List of words of gold corpus
    Output: list of each syllable followed by the proper tag
    Eg:
    Input: ['ལ་', 'ལ་ལ་', 'ལ་', 'ལ་བ་'], gold_index=0, gold_index_track =3
    Output: ['ལ་', 'N', 'ལ་','N', 'ལ་', 'C', 'ལ་']

    N: means start of new word
    C: Continuation of the previous word
    """
    gold_corpus_unmatched_word_list = gold_corpus_words[gold_index:gold_index_track]
    gold_corpus_syls_tagged = []

    for gold_corpus_unmatched_word in gold_corpus_unmatched_word_list:

        gold_corpus_unmatched_syls = split_by_TSEK(gold_corpus_unmatched_word)

        new_word = True
        for gold_corpus_unmatched_syl in gold_corpus_unmatched_syls:
            gold_corpus_syls_tagged.append(gold_corpus_unmatched_syl + TSEK)
            if new_word:
                gold_corpus_syls_tagged.append("N")
                new_word = False
            else:
                gold_corpus_syls_tagged.append("C")
    return gold_corpus_syls_tagged


def tagger(file_string):
    equal_number_of_syls, gold_corpus_output, botok_output = comparator(file_string)
    if equal_number_of_syls is False:
        return "ValueError: Output of gold corpus and botok output does not match."

    pattern = r"[ ]+"
    replacement = " "

    gold_corpus_output = re.sub(pattern, replacement, gold_corpus_output.strip())
    botok_output = re.sub(pattern, replacement, botok_output.strip())

    gold_corpus_words = gold_corpus_output.split()
    botok_words = botok_output.split()
    botok_words_count = len(botok_words)

    gold_index = 0
    botok_index = 0
    tagged_content = ""
    while botok_index < botok_words_count:
        condition1 = botok_words[botok_index] == gold_corpus_words[gold_index]
        condition2 = botok_index == 0 or (
            "".join(botok_words[:botok_index])
            == "".join(gold_corpus_words[:gold_index])
        )
        # If the word matches perfectly in output of both botok and gold corpus
        if condition1 and condition2:
            tagged_content += botok_words[botok_index] + "/P "
            gold_index += 1
            botok_index += 1
            continue

        gold_index_track = gold_index
        botok_index_track = botok_index
        # Find the occurence of the next perfect word that matches in output of both botok and gold corpus
        while not (
            (botok_words[botok_index_track] == gold_corpus_words[gold_index_track])
            and (
                "".join(botok_words[botok_index : botok_index_track + 1])  # noqa
                == "".join(gold_corpus_words[gold_index : gold_index_track + 1])  # noqa
            )
        ):
            botok_unmatched_words = "".join(
                botok_words[botok_index : botok_index_track + 1]  # noqa
            )
            gold_corpus_unmatched_words = "".join(
                gold_corpus_words[gold_index : gold_index_track + 1]  # noqa
            )

            botok_unmatched_syls = split_by_TSEK(botok_unmatched_words)
            gold_corpus_unmatched_syls = split_by_TSEK(gold_corpus_unmatched_words)

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
            botok_unmatched_syls = split_by_TSEK(botok_unmatched_word)
            botok_unmatched_syls_count = len(botok_unmatched_syls)
            botok_syls = ""
            botok_tags = ""

            for i in range(
                gold_corpus_syls_tagged_index,
                (gold_corpus_syls_tagged_index + (2 * botok_unmatched_syls_count)),
                2,
            ):
                botok_syls += gold_corpus_syls_tagged[i]
                botok_tags += gold_corpus_syls_tagged[i + 1]

            tagged_content += botok_syls + "/" + botok_tags + " "
            gold_corpus_syls_tagged_index = gold_corpus_syls_tagged_index + (
                2 * botok_unmatched_syls_count
            )

        gold_index = gold_index_track
        botok_index = botok_index_track

    return tagged_content


if __name__ == "__main__":
    # tagger("༄༅། །རྒྱལ་པོ་ ལ་ གཏམ་ བྱ་བ་ རིན་པོ་ཆེ-འི་ hello ཕྲེང་བ། །ཡོན་ཏན་ ཀུན་ གྱིས་ བརྒྱན་པ་+པོ།")
    pass
