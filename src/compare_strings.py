from .data_processor import transform_gold_corpus_for_tagging
from .tokenizer_pipeline import botok_word_tokenizer_pipeline
from .Utility.regex_replacer import replace_with_regex


def is_corpus_tokenization_identical(gold_corpus_string, botok_output_string):
    pattern = {" ": "_", "-": "", "_": ""}
    gold_corpus_without_spaces = replace_with_regex(pattern, gold_corpus_string)
    botok_output_string_without_spaces = replace_with_regex(
        pattern, botok_output_string
    )

    equal_string_length = len(gold_corpus_without_spaces) == len(
        botok_output_string_without_spaces
    )
    return equal_string_length


def compare_gold_corpus_and_tokenized_output(gold_corpus):
    gold_corpus_output = transform_gold_corpus_for_tagging(gold_corpus)
    botok_output = botok_word_tokenizer_pipeline(gold_corpus)

    equal_number_of_syls = is_corpus_tokenization_identical(
        gold_corpus_output, botok_output
    )
    return equal_number_of_syls, gold_corpus_output, botok_output
