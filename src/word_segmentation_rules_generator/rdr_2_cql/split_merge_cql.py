import copy

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


def make_split_cql_rule(
    syllable_word_list, syllable_tag_list, word_index, syllable_index
):
    """
    each cql rule should be as follows: <matchcql>\t<index>\t<operation>\t<replacecql>
    cql example :
    ["ལ་ལ་"] ["ལ་ལ་"]	1-2	::	[] []
    ["ལ་"] ["ལ་"] ["ལ་ལ་"]	3-2	::	[] []
    ["ལ་"] ["ལ་"] ["ལ་"] ["ལ་"]	2	+	[]
    """

    matchcql = ""
    matching_index = word_index + 1
    if syllable_index == 0:
        syllable_index = 1
    splitting_index = len("".join(syllable_word_list[word_index][:syllable_index]))
    index = f"{matching_index}-{splitting_index}"
    operation = "::"
    replacecql = "[] []"

    for i in range(len(syllable_word_list)):
        matchcql += "[text={}] ".format("".join(syllable_word_list[i]))

    new_cql_rule = "\t".join([matchcql, index, operation, replacecql])
    print(new_cql_rule)
    print(syllable_word_list)
    print(syllable_tag_list)


def split_inner_list(lst, i, j):
    if i < 0 or i >= len(lst):
        raise ValueError("Index i is out of range.")
    if j < 0 or j >= len(lst[i]):
        raise ValueError("Index j is out of range.")

    split_list = lst[i].pop(j)
    lst.insert(i + 1, [split_list])

    return lst


def get_new_indices(my_list, new_list, old_i, old_j):
    # Returns new_indices of new_list with respect to original_list indices
    if old_i < 0 or old_i >= len(my_list):
        raise ValueError("Old index i is out of range.")
    if old_j < 0 or old_j >= len(my_list[old_i]):
        raise ValueError("Old index j is out of range.")

    num_elements_passed = 0
    found = False

    for outer_index, inner_list in enumerate(my_list):
        for inner_index, element in enumerate(inner_list):
            if outer_index == old_i and inner_index == old_j:
                found = True
                break
            num_elements_passed += 1
        if found:
            break

    new_elements_passed = 0
    new_i, new_j = 0, 0
    found = False

    for outer_index, inner_list in enumerate(new_list):
        for inner_index, element in enumerate(inner_list):
            if new_elements_passed == num_elements_passed:
                found = True
                new_i = outer_index
                new_j = inner_index
                break
            new_elements_passed += 1
        if found:
            break

    return new_i, new_j


def make_merge_cql_rule(
    syllable_word_list, syllable_tag_list, word_index, syllable_index
):
    pass


def make_cql_rule(syllable_word_list, syllable_tag_list, new_word_index, end_index):
    syllable_word_list = syllable_word_list[new_word_index:end_index]
    syllable_tag_list = syllable_tag_list[new_word_index:end_index]

    # Create a deep copy of the list to avoid modifying the original list
    syls_word_list = copy.deepcopy(syllable_word_list)
    syls_tag_list = copy.deepcopy(syllable_tag_list)

    new_i, new_j = 0, 0
    # first performing split function
    new_word_started = False
    for i in range(len(syllable_tag_list)):
        # curr_word means current word
        curr_word_list = syllable_tag_list[i]
        for j in range(len(curr_word_list)):
            if not new_word_started:
                new_word_started = True
                continue
            if syllable_tag_list[i][j] in ["N", "A"]:
                new_i, new_j = get_new_indices(syllable_word_list, syls_word_list, i, j)
                make_split_cql_rule(syls_word_list, syls_tag_list, new_i, new_j)
                # Break down the rules
                syls_word_list = split_inner_list(syls_word_list, new_i, new_j)
                syls_tag_list = split_inner_list(syls_tag_list, new_i, new_j)

    # Second performing merge function

    # Create a deep copy of the list to avoid modifying the original list

    syls_word_list_for_merge = copy.deepcopy(syls_word_list)
    syls_tag_list_for_merge = copy.deepcopy(syls_tag_list)
    new_i, new_j = 0, 0

    for i in range(len(syls_tag_list) - 1):
        curr_tag_list = syls_tag_list[i + 1]
        if curr_tag_list[0] in ["C", "B"]:
            new_i, new_j = get_new_indices(
                syls_word_list, syls_word_list_for_merge, i, j
            )
            make_merge_cql_rule(
                syls_tag_list_for_merge, syls_tag_list_for_merge, new_i, new_j
            )


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
        Another example:
        [['བཀྲ་', 'ཤིས་', 'ཤོག']]
        [['N', 'C', 'N']]
        """

        words_count = len(syllable_word_list)

        new_word_index = -1
        for i in range(words_count):
            if syllable_tag_list[i][0] in ["N", "A"] and new_word_index != -1:
                make_cql_rule(syllable_word_list, syllable_tag_list, new_word_index, i)
                new_word_index = i
        if new_word_index == -1:
            make_cql_rule(syllable_word_list, syllable_tag_list, 0, words_count)


def split_merge_cql(tagged_string):
    word_list, tag_list = tagged_string_to_word_tag_list(tagged_string)
    tag_split_list = split_tag_list_with_index(tag_list)
    find_words_for_split_merge(tag_split_list, word_list, tag_list)
    # return tag_split_list
