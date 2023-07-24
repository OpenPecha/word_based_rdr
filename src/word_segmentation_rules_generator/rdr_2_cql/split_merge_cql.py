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


def split_merge_cql(tagged_string):
    word_list, tag_list = tagged_string_to_word_tag_list(tagged_string)
    tag_split_list = split_tag_list_with_index(tag_list)
    return tag_split_list
