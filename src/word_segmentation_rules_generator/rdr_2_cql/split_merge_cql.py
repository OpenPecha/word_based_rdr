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


def split_merge_cql(tagged_string):
    word_list, tag_list = tagged_string_to_word_tag_list(tagged_string)
    start_index = -1
    for i in range(len(tag_list)):
        if tag_list[i] == "P" and start_index == -1:
            continue
        if tag_list[i] == "P" and start_index != -1:
            make_cql_rule(start_index, i, word_list, tag_list)
            start_index = -1
        if start_index == -1:
            start_index = i
        if "C" in tag_list[i] or "B" in tag_list[i]:
            make_cql_rule(start_index, i, word_list, tag_list)
            start_index = -1
