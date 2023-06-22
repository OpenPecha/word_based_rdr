from ..max_matcher.max_matcher import botok_max_matcher
from ..preprocessing.preprocessor import gold_corpus_2_tagger


def is_equal_string_length(gold_corpus_string, botok_output_string):
    gold_corpus_without_spaces = gold_corpus_string.replace(" ", "").replace("_", "").replace("-","")
    botok_output_string_without_spaces = botok_output_string.replace(" ", "").replace("_", "").replace("-","")

    equal_string_length = len(gold_corpus_without_spaces) == len(
        botok_output_string_without_spaces
    )
    return equal_string_length


def comparator(file_string):
    # Comparing if the string out(gold corpus and max match output) going for tagging has the same number of syllables
    gold_corpus_output = gold_corpus_2_tagger(file_string)
    botok_output = botok_max_matcher(file_string)

    equal_number_of_syls = is_equal_string_length(gold_corpus_output, botok_output)
    return equal_number_of_syls, gold_corpus_output, botok_output
