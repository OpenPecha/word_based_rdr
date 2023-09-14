from ..botok_word_tokenizer_pipeline import botok_word_tokenizer_pipeline
from ..data_processor import transform_gold_corpus_for_tagging


def is_equal_string_length(gold_corpus_string, botok_output_string):
    gold_corpus_without_spaces = (
        gold_corpus_string.replace(" ", "").replace("_", "").replace("-", "")
    )
    botok_output_string_without_spaces = (
        botok_output_string.replace(" ", "").replace("_", "").replace("-", "")
    )

    equal_string_length = len(gold_corpus_without_spaces) == len(
        botok_output_string_without_spaces
    )
    return equal_string_length


def comparator(file_string):
    # Comparing if the string out(gold corpus and max match output) going for tagging has the same number of syllables
    gold_corpus_output = transform_gold_corpus_for_tagging(file_string)
    botok_output = botok_word_tokenizer_pipeline(file_string)

    equal_number_of_syls = is_equal_string_length(gold_corpus_output, botok_output)
    return equal_number_of_syls, gold_corpus_output, botok_output
