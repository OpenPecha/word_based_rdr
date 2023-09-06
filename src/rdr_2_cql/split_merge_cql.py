import sys
from itertools import combinations
from pathlib import Path
from typing import Dict, List

# Add the root directory of your project to sys.path
root_path = (
    Path(__file__).resolve().parents[2]
)  # Adjust the number of parents as needed
sys.path.append(str(root_path))

from src.rdr_2_cql.rdr_2_replace_matcher import find_levels, find_rules  # noqa
from src.tagger.tagger import split_by_TSEK  # noqa
from src.Utility.get_POS import get_POS  # noqa


def make_split_cql_rule(rdr_condition_list, object_word_index, rdr_conclusion):
    """
    Example for the arguments
    rdr_condition_list:  [[('object.word', '"ལ་ལ་"')], [('object.nextWord', '"ལ་ལ་"')]]
    object_word_index: 0
    rdr_conclusion: 'BB'
    """

    """
    each cql rule should be as follows: <matchcql>\t<index>\t<operation>\t<replacecql>
    cql example :
    ["ལ་ལ་"] ["ལ་ལ་"]	1-2	::	[] []
    ["ལ་"] ["ལ་"] ["ལ་ལ་"]	3-2	::	[] []
    ["ལ་"] ["ལ་"] ["ལ་"] ["ལ་"]	2	+	[]
    """

    matchcql = ""
    for rdr_condition in rdr_condition_list:
        matchcql += "["
        for rdr_attribute in rdr_condition:
            if "word" in rdr_attribute[0] or "Word" in rdr_attribute[0]:
                matchcql += f"{rdr_attribute[1]}"
            elif "pos" in rdr_attribute[0] or "Pos" in rdr_attribute[0]:
                matchcql += f"pos={rdr_attribute[1]}"
        matchcql += "] "

    # Get the value for object.word
    object_word = next(  # noqa
        (
            attr_value[1]
            for attr_value in rdr_condition_list[object_word_index]
            if attr_value[0] == "object.word"
        ),
        None,
    )

    object_word_list = split_by_TSEK(object_word)
    rdr_conclusion_list = list(rdr_conclusion)

    splited_left_word = splited_right_word = ""
    splited_left_pos = splited_right_pos = ""
    for i in range(1, len(rdr_condition_list)):
        if rdr_conclusion_list[i] in ["B", "X"]:
            splited_left_word = "".join(object_word_list[:i])
            splited_right_word = "".join(object_word_list[i:])
            break

    matching_index = object_word_index + 1
    splitting_index = len(splited_left_word)
    index = f"{matching_index}-{splitting_index}"

    # Getting POS tag of the splited words
    splited_left_pos = get_POS(splited_left_word)
    splited_right_pos = get_POS(splited_right_word)

    operation = "::"
    replacecql = f"[pos={splited_left_pos}] [pos={splited_right_pos}]"

    new_cql_rule = "\t".join([matchcql, index, operation, replacecql])
    return new_cql_rule


def find_combinations_of_matches(list_of_dicts):
    # Create a dictionary to group frozensets of dictionaries by their hash values

    dict_matched_groups: List[Dict] = []
    dict_matched_indices: List[List[int]] = []

    for idx, curr_dict in enumerate(list_of_dicts):
        # Convert the dictionary to a frozenset to make it hashable

        if curr_dict in dict_matched_groups:
            matched_index = dict_matched_groups.index(curr_dict)
            dict_matched_indices[matched_index].append(idx)
        else:
            dict_matched_groups.append(curr_dict)
            dict_matched_indices.append([idx])

    # Find all combinations of indices where dictionaries are the same
    all_combinations = []
    for indices in dict_matched_indices:
        if len(indices) >= 2:
            for r in range(
                2, len(indices) + 1
            ):  # Consider combinations of size 2, 3, and so on
                for combination in combinations(indices, r):
                    all_combinations.append(combination)

    return all_combinations


def check_for_tag_rule_condition(matched_indices, rdr_conclusion_storage):
    # matched_indices: list of tuples [(0,1), (3,6)]
    # rdr_conclusion_storage: list of tuples [(0,'"B"'),((0,'"B"'))]
    for match_index_tuple in matched_indices:
        matched_rdr_conclusion = []
        for matched_index in match_index_tuple:
            matched_rdr_conclusion.append(rdr_conclusion_storage[matched_index])
        print(matched_rdr_conclusion, "    ", match_index_tuple)


def filter_neccessary_rdr_rules(rdr_string):

    # Gets rdr rules with levels  <---Level 0
    # True : object.conclusion = "NN"   <---Level 1
    #        object.tag == "U" : object.conclusion = "U"    <---Level 2
    #                object.word == "མི་" and object.pos == "VERB" : object.conclusion = "B" <---Level 3
    # 		                  object.word == "མི་" and object.nextWord1 == "ཕན་" : object.conclusion = "U"   <---Level 4
    rdr_rules_with_levels = find_levels(rdr_string)
    rdr_rules_count = len(rdr_rules_with_levels)
    index = 0

    # In this function we putting rules with more than level 2 above the level 2, for split merge
    while index < rdr_rules_count:
        rdr_level = rdr_rules_with_levels[index]
        if rdr_level[0] > 2:
            start_index = index - 1
            end_index = index
            while rdr_rules_with_levels[end_index][0] > 2:
                end_index += 1
            end_index -= 1
            # Reversing the rules
            rdr_rules_with_levels[
                start_index : end_index + 1  # noqa
            ] = rdr_rules_with_levels[
                start_index : end_index + 1  # noqa
            ][
                ::-1
            ]
            index = end_index + 1
        else:
            index += 1

    rdr_rules = find_rules(rdr_rules_with_levels)

    # Deleting the first rdr rules which is unneccessary
    # 	object.tag == "U" : object.conclusion = "U" (looks like this in the .RDR)
    del rdr_rules[0]

    # Unneccessary tuple
    tuple_to_remove = ("object.tag", '"U"')

    sorted_rdr_condition_storage = []
    sorted_rdr_conclusion_storage = []

    # In this code, what we are trying to achieve is, check for matches of rdr rules
    # EG: take look for following two rdr rules, those two should be matched together along with their tag
    # object.word == "ལ་ལ་" and object.nextWord1 == "ལ་ལ་" : object.conclusion = "BB"
    # object.prevWord1 == "ལ་ལ་" and object.word == "ལ་ལ་" : object.conclusion = "IB"
    for rdr_rule in rdr_rules:
        # Deleting the unnecessary 'object.tag' attribute
        rdr_rule["test"][0].remove(tuple_to_remove)

        # Getting the index of attributes of rdr rules
        rdr_attributes_indices = list(rdr_rule["test"].keys())
        rdr_attributes_indices.sort()

        attr_counter = 0
        rdr_condition_storage = {}
        # Looping through each rdr_condition
        # attrs_index = -1, for object.prevWord1 and object.prevPos1
        # attrs_index = 0, for object.word and object.pos
        # attrs_index=1, for object.nextWord1 and object.nextPos1:
        for attrs_index in rdr_attributes_indices:
            curr_index_attributes = rdr_rule["test"][attrs_index]

            # When attrs_index 0 comes, store the tag value
            if attrs_index == 0:
                sorted_rdr_conclusion_storage.append(
                    (attr_counter, rdr_rule["ccl"][0][0][1])
                )
            attrs_storage = {}
            for attr_tuple in curr_index_attributes:
                if "word" in attr_tuple[0].lower():
                    # attrs_storage.append(("TEXT", attr_tuple[1]))
                    attrs_storage["TEXT"] = attr_tuple[1]
                    continue
                if "pos" in attr_tuple[0].lower():
                    # attrs_storage.append(("POS", attr_tuple[1]))
                    attrs_storage["POS"] = attr_tuple[1]

            rdr_condition_storage[attr_counter] = attrs_storage
            attr_counter += 1

        sorted_rdr_condition_storage.append(rdr_condition_storage)

    # Recieves indices where the rdr condition matches (list of tuples)
    matched_indices = find_combinations_of_matches(sorted_rdr_condition_storage)

    # result = check_for_tag_rule_condition(
    #     matched_indices, sorted_rdr_conclusion_storage
    # )
    return matched_indices


def split_merge_cql(rdr_string):
    rdr_rules = find_rules(find_levels(rdr_string))
    for rdr_rule in rdr_rules:
        rdr_condition = rdr_rule["test"]
        rdr_conclusion = rdr_rule["ccl"][0][0][1]

        # Checking for Tag intro (not an actual rule)
        # 	object.tag == "U" : object.conclusion = "U" (looks like this in the .RDR)
        if len(rdr_condition) == 1 and len(rdr_condition[0]) == 1:
            continue

        condition_count = len(rdr_condition)

        # Store rdr condition aside from tag
        rdr_condition_list = []
        # Store the index where object.word is present
        object_word_index = -1
        for i in range(condition_count):
            curr_rdr_condition = rdr_condition[i]
            attribute_condition_count = len(curr_rdr_condition)
            attribute_condition_list = []
            for j in range(attribute_condition_count):
                if curr_rdr_condition[j][0] == "object.tag":
                    continue
                if curr_rdr_condition[j][0] == "object.word":
                    object_word_index = i
                attribute_condition_list.append(curr_rdr_condition[j])
            rdr_condition_list.append(attribute_condition_list)
        cql_rule = make_split_cql_rule(
            rdr_condition_list, object_word_index, rdr_conclusion
        )
        print(cql_rule)
    return rdr_rules


if __name__ == "__main__":
    rdr_string = Path("src/data/TIB_train_maxmatched_tagged.txt.RDR").read_text(
        encoding="utf-8"
    )
    # rdr_rules = split_merge_cql(rdr_string)
    rdr_rules = filter_neccessary_rdr_rules(rdr_string)
