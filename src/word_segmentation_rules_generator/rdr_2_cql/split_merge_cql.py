from ..RDRPOSTagger.Utility.Utils import getWordTag


def tagged_string_to_word_tag_list(tagged_string):
    word_list = []
    tag_list = []

    for tagged_word in tagged_string.split():
        word, tag = getWordTag(tagged_word)
        word_list.append(word)
        tag_list.append(tag)

    return word_list, tag_list
