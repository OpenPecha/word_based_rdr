from src.word_segmentation_rules_generator.tagger.tagger import split_by_TSEK

from ..RDRPOSTagger.Utility.Utils import getWordTag


def tagged_string_to_word_tag_list(tagged_string):
    word_list = []
    tag_list = []

    for tagged_word in tagged_string.split():
        word, tag = getWordTag(tagged_word)
        word_list.append(word)
        tag_list.append(tag)

    return word_list, tag_list


def make_cql_rule(start_index, i, word_list, tag_list):
    pass


def split_tag_list_with_index(tag_list):
    tag_split_list = []
    start_index = -1
    for i in range(len(tag_list)):
        if tag_list[i] == "P" and start_index == -1:
            continue
        if tag_list[i] == "P" and start_index != -1:
            tag_split_list.append((start_index, i - 1))
            start_index = -1
            continue
        if start_index == -1 and tag_list[i] != "P":
            start_index = i
    return tag_split_list


def find_words_for_split_merge(tag_split_list, word_list, tag_list):
    for tuple_index in tag_split_list:
        start_index, stop_index = tuple_index
        syllable_word_list = []
        syllable_tag_list = []
        for i in range(start_index, stop_index + 1):
            syllable_word_list.append(split_by_TSEK(word_list[i]))
            syllable_tag_list.append(list(tag_list[i]))
        """
        syllable_word_list = [[ལ་,ལ་],[ལ་,ལ་]]
        syllable_tag_list = [['N','N'],['C','N']]
        """

        words_count = len(syllable_word_list)
        new_word_index = 0
        for i in range(words_count):
            if syllable_tag_list[i][0] in ["N", "A"] and new_word_index != 0:
                make_cql_rule(syllable_word_list, syllable_tag_list, new_word_index, i)
                new_word_index = i


def split_merge_cql(tagged_string):
    word_list, tag_list = tagged_string_to_word_tag_list(tagged_string)
    tag_split_list = split_tag_list_with_index(tag_list)
    find_words_for_split_merge(tag_split_list, word_list, tag_list)
    # return tag_split_list
