from botok import WordTokenizer

from rules_generator.data_processor import transform_gold_corpus_for_tagging
from rules_generator.tokenizer_pipeline import botok_word_tokenizer_pipeline
from rules_generator.Utility.regex_replacer import replace_with_regex


def is_corpus_tokenization_identical(gold_corpus, tokenized_output):
    # here spaces are replaced with underscore to compare if syllables are separated correctly
    pattern = {" ": "_", "-": "", "_": ""}
    gold_corpus = replace_with_regex(pattern, gold_corpus)
    botok_output = replace_with_regex(pattern, tokenized_output)

    is_syllables_separated_correctly = len(gold_corpus) == len(botok_output)
    return is_syllables_separated_correctly


def compare_gold_corpus_and_tokenized_output(gold_corpus):
    gold_corpus_cleaned = transform_gold_corpus_for_tagging(gold_corpus)
    tokenized_output = botok_word_tokenizer_pipeline(WordTokenizer(), gold_corpus)

    is_syllables_separated_correctly = is_corpus_tokenization_identical(
        gold_corpus_cleaned, tokenized_output
    )
    return is_syllables_separated_correctly, gold_corpus_cleaned, tokenized_output
