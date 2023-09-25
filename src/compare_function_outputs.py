from .botok_tokenizer_pipeline import botok_word_tokenizer_pipeline
from .data_processor import transform_gold_corpus_for_tagging
from .Utility.regex_replacer import replace_with_regex


def is_equal_string_length(gold_corpus_string, botok_output_string):
    pattern = {" ": "_", "-": "", "_": ""}
    gold_corpus_without_spaces = replace_with_regex(pattern, gold_corpus_string)
    botok_output_string_without_spaces = replace_with_regex(
        pattern, botok_output_string
    )

    equal_string_length = len(gold_corpus_without_spaces) == len(
        botok_output_string_without_spaces
    )
    return equal_string_length


def compare_function_outputs(file_string):
    # Comparing if the string out(gold corpus and max match output) going for tagging has the same number of syllables
    gold_corpus_output = transform_gold_corpus_for_tagging(file_string)
    botok_output = botok_word_tokenizer_pipeline(file_string)

    equal_number_of_syls = is_equal_string_length(gold_corpus_output, botok_output)
    return equal_number_of_syls, gold_corpus_output, botok_output
