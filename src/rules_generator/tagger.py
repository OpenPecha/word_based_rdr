from pathlib import Path
from typing import List, Tuple

from botok import TSEK

from rules_generator.annotation_transfer import newline_annotations_transfer
from rules_generator.data_processor import transform_gold_corpus_for_tagging
from rules_generator.tokenizer_pipeline import botok_word_tokenizer_pipeline
from rules_generator.Utility.get_syllables import get_syllables


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


def filter_underscore(text: str) -> str:
    return text.replace("_", "")


def filter_hyphen(text: str) -> str:
    return text.replace("-", "")


def find_next_matching_words(
    tokenized_words: List[str],
    gold_corpus_words: List[str],
    tok_idx: int,
    gold_idx: int,
) -> Tuple[int, int]:
    """
    Find the next matching words between botok and gold corpus starting from given indices.
    Returns the indices of the last matching words found.
    """
    gold_last_idx, tok_last_idx = gold_idx, tok_idx

    while tok_last_idx < len(tokenized_words) and gold_last_idx < len(
        gold_corpus_words
    ):

        curr_tok_word = filter_underscore(tokenized_words[tok_last_idx])
        curr_gold_word = filter_underscore(gold_corpus_words[gold_last_idx])

        condition_1 = curr_tok_word == curr_gold_word

        unmatched_tok_words = "".join(
            tokenized_words[i] for i in range(tok_idx, tok_last_idx + 1)
        )
        unmatched_gold_words = "".join(
            gold_corpus_words[i] for i in range(gold_idx, gold_last_idx + 1)
        )

        unmatched_tok_words = filter_underscore(filter_hyphen(unmatched_tok_words))
        unmatched_gold_words = filter_underscore(filter_hyphen(unmatched_gold_words))

        condition2 = unmatched_tok_words == unmatched_gold_words
        if condition_1 and condition2:
            break

        unmatched_tok_syls = split_words_into_syllables(
            [tokenized_words[i] for i in range(tok_idx, tok_last_idx + 1)]
        )

        unmatched_gold_syls = split_words_into_syllables(
            [gold_corpus_words[i] for i in range(gold_idx, gold_last_idx + 1)]
        )

        if len(unmatched_tok_syls) > len(unmatched_gold_syls):
            gold_last_idx += 1
        elif len(unmatched_tok_syls) < len(unmatched_gold_syls):
            tok_last_idx += 1
        else:
            gold_last_idx += 1
            tok_last_idx += 1

    return gold_last_idx, tok_last_idx


def tag_unmatched_words(
    tokenized_words: List[str],
    gold_corpus_words: List[str],
    tok_idx: int,
    gold_idx: int,
) -> Tuple[str, int, int]:
    """
    Tag unmatched words based on gold corpus syllables and return the tagged content.
    Returns the tagged content and the indices after tagging.
    """
    gold_last_idx, tok_last_idx = find_next_matching_words(
        tokenized_words, gold_corpus_words, tok_idx, gold_idx
    )

    tagged_gold_syls = tag_syllables(gold_corpus_words[gold_idx:gold_last_idx])

    unmatched_tokenized_words = tokenized_words[tok_idx:tok_last_idx]

    tagged_gold_idx = 0
    tagged_content = ""

    for unmatched_tokenized_word in unmatched_tokenized_words:
        unmatched_tokenzied_syls = get_syllables(unmatched_tokenized_word)
        unmatched_tokenzied_syls_count = len(unmatched_tokenzied_syls)
        tokenized_syls = ""
        tokenized_tags = ""

        unmatched_tok_idx = 0

        for i in range(
            tagged_gold_idx,
            tagged_gold_idx + (2 * unmatched_tokenzied_syls_count),
            2,
        ):
            tokenized_syls += unmatched_tokenzied_syls[unmatched_tok_idx]
            unmatched_tok_idx += 1
            tokenized_tags += tagged_gold_syls[i + 1]

        tagged_content += tokenized_syls + "/" + tokenized_tags + " "
        tagged_gold_idx = tagged_gold_idx + (2 * unmatched_tokenzied_syls_count)

    return tagged_content, gold_last_idx, tok_last_idx


def tagger(gold_corpus: str) -> str:
    tokenized_output = botok_word_tokenizer_pipeline(gold_corpus)
    gold_corpus_cleaned = transform_gold_corpus_for_tagging(gold_corpus)
    gold_corpus_cleaned = newline_annotations_transfer(
        tokenized_output, gold_corpus_cleaned
    )

    gold_corpus_lines = gold_corpus_cleaned.splitlines()
    tokenized_lines = tokenized_output.splitlines()

    if len(gold_corpus_lines) != len(tokenized_lines):
        return (
            "Error: Number of lines in gold corpus and tokenized output does not match."
        )

    tagged_content = ""

    # Now, process the content line by line
    for line_idx in range(len(gold_corpus_lines)):
        try:  # try block added here
            gold_line_words = gold_corpus_lines[line_idx].split()
            tokenized_line_words = tokenized_lines[line_idx].split()

            gold_idx, tok_idx = 0, 0

            while tok_idx < len(tokenized_line_words) and gold_idx < len(
                gold_line_words
            ):
                curr_tok_word = filter_underscore(tokenized_line_words[tok_idx])
                curr_gold_word = filter_underscore(gold_line_words[gold_idx])

                if curr_tok_word == curr_gold_word:
                    tagged_content += tokenized_line_words[tok_idx] + "/U "
                    gold_idx += 1
                    tok_idx += 1
                    continue

                unmatched_tagged_content, gold_idx, tok_idx = tag_unmatched_words(
                    tokenized_line_words, gold_line_words, tok_idx, gold_idx
                )
                tagged_content += unmatched_tagged_content

            tagged_content += (
                "\n"  # At the end of each line, add a newline to separate the lines
            )

        except Exception as e:  # except block added here
            print(f"An error occurred at line {line_idx + 1}: {e}")
            # Optionally, log the error details somewhere for review.

            # If you don't want to interrupt the loop, continue to the next iteration.
            continue

    return (
        tagged_content.strip()
    )  # Use strip to remove the trailing newline if necessary


if __name__ == "__main__":
    file_string = Path("src/data/TIB_train.txt").read_text(encoding="utf-8")
    tagged_output = tagger(file_string)
    with open("src/data/TIB_tagged.txt", "w", encoding="utf-8") as file:
        file.write(tagged_output)
