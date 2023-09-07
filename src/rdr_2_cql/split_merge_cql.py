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
from src.Utility.get_POS import get_POS, get_word_senses  # noqa
from src.Utility.split_by_TSEK import split_by_TSEK  # noqa

NO_POS = "NO_POS"
empty_POS = '"'


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


def Re_Arrange_the_ordering(rdr_rules_with_levels):
    rdr_rules_count = len(rdr_rules_with_levels)
    index = 0

    # In this function we putting rules with more than level 2 above the level 2, for split merge
    # object.word == "མི་" and object.pos == "VERB" : object.conclusion = "B" <---Level 2
    #       object.word == "མི་" and object.nextWord1 == "ཕན་" : object.conclusion = "U"   <---Level 3
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
    return rdr_rules_with_levels


def filter_only_neccessary_rdr_rules(rdr_string):

    # Gets rdr rules with levels
    # True : object.conclusion = "NN"   <---Level 0
    #        object.tag == "U" : object.conclusion = "U"    <---Level 1
    #                object.word == "མི་" and object.pos == "VERB" : object.conclusion = "B" <---Level 2
    # 		                  object.word == "མི་" and object.nextWord1 == "ཕན་" : object.conclusion = "U"   <---Level 3
    rdr_rules_with_levels = find_levels(rdr_string)

    # In this function we putting rules with more than level 2 above the level 2, for split merge
    ordered_rdr_rules_with_levels = Re_Arrange_the_ordering(rdr_rules_with_levels)
    # Then find the rdr rules
    rdr_rules = find_rules(ordered_rdr_rules_with_levels)

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
                    # attrs_storage.append(("text", attr_tuple[1]))
                    attrs_storage["text"] = attr_tuple[1]
                    continue
                if "pos" in attr_tuple[0].lower():
                    # attrs_storage.append(("pos", attr_tuple[1]))
                    attrs_storage["pos"] = attr_tuple[1]

            rdr_condition_storage[attr_counter] = attrs_storage
            attr_counter += 1

        sorted_rdr_condition_storage.append(rdr_condition_storage)

    # Recieves indices where the rdr condition matches (list of tuples, tuples containing the matched elements together)
    matched_indices = find_combinations_of_matches(sorted_rdr_condition_storage)

    # unique_matched_indices = list(set(item for tpl in matched_indices for item in tpl))
    # #Appending rest of the rules as well one by one
    # matched_indices.extend((i,) for i in range(len(sorted_rdr_condition_storage)) if i not in unique_matched_indices)

    # Filtering rules that were only on the matched_indices
    final_filtered_rdr_rules = []
    for matched_index_tuple in matched_indices:
        curr_rdr_rule_conclusion = []
        for matched_index in matched_index_tuple:
            curr_rdr_rule_conclusion.append(
                sorted_rdr_conclusion_storage[matched_index]
            )
        final_filtered_rdr_rules.append(
            [
                sorted_rdr_condition_storage[matched_index_tuple[0]],
                curr_rdr_rule_conclusion,
            ]
        )

    return final_filtered_rdr_rules


def split_merge_cql(rdr_string):
    rdr_rules = filter_only_neccessary_rdr_rules(rdr_string)
    cql_rules_collection = ""
    for idx, rdr_rule in enumerate(rdr_rules):
        rdr_condition = rdr_rule[0]
        rdr_conclusion = rdr_rule[1]

        # Sorting the rdr conclusion based on the index, element
        rdr_conclusion = sorted(rdr_conclusion, key=lambda x: x[0])

        # If the particular rules doesn't has proper format
        is_unnecessary_rule = False

        # Checking for affix rule generation
        for rdr_conclusion_tuple in rdr_conclusion:
            rdr_conclusion_tag = rdr_conclusion_tuple[1]

            # Getting tag of each syls for checking if affix rules generation is needed
            # rdr_condition_syls = ['"ངེས་', 'པར་'],
            # rdr_conclusion_tag_list = ['B', 'Y']
            rdr_condition_text = rdr_condition[rdr_conclusion_tuple[0]]["text"]
            rdr_condition_syls = split_by_TSEK(rdr_condition_text)

            rdr_conclusion_tag_list = list(rdr_conclusion_tag)

            # Cleaning empty elements after conversion from word to syls
            rdr_condition_syls = [x for x in rdr_condition_syls if x != "" and x != '"']
            rdr_conclusion_tag_list = [
                x for x in rdr_conclusion_tag_list if x != "" and x != '"'
            ]

            # check if each syllables has their corresponding tag
            if len(rdr_condition_syls) != len(rdr_conclusion_tag_list):
                is_unnecessary_rule = True
                break

            need_affix_rule_generation = False
            # if there is a need for affix modification, this will store index, and operation in tuple
            affix_modification = []
            for idx_for_affix, curr_syl in enumerate(rdr_condition_syls):
                if "-" in curr_syl and rdr_conclusion_tag_list[idx_for_affix] not in [
                    "X",
                    "Y",
                ]:
                    need_affix_rule_generation = True
                    affix_modification.append((idx_for_affix, "OFF"))
                    continue
                if "-" not in curr_syl and rdr_conclusion_tag_list in ["X", "Y"]:
                    need_affix_rule_generation = True
                    affix_modification.append((idx_for_affix, "OFF"))
            if need_affix_rule_generation:
                affix_rule = generate_affix_rule(
                    rdr_condition, rdr_conclusion, affix_modification
                )
                cql_rules_collection += f"{affix_rule}\n"

        # if the rule is not proper, jumps to next rule
        if is_unnecessary_rule:
            continue

        # Checking for split rule generation

    return cql_rules_collection


def generate_affix_rule(rdr_condition, rdr_conclusion, affix_modification):
    """
    each cql rule should be as follows: <matchcql>\t<index>\t<operation>\t<replacecql>
    cql example :
    ["ལ་ལ་"] ["ལ་ལ་"]	1-2	::	[] []
    ["ལ་"] ["ལ་"] ["ལ་ལ་"]	3-2	::	[] []
    ["ལ་"] ["ལ་"] ["ལ་"] ["ལ་"]	2	+	[]
    [""]    1   +   []
    """

    # Collecting all the cql rule string
    affix_cql_rules_collection = ""
    for idx, afx_modf in affix_modification:
        word_text = rdr_condition[idx]["text"]
        word_text = word_text.replace("-", "")[
            1:-1
        ]  # removing '-' before passing the string to find POS
        word_pos = get_POS(word_text)
        word_senses = get_word_senses(word_text)

        # If there is no word sense present or POS is empty, then no rule is generated
        if not word_senses or word_pos in [NO_POS, empty_POS]:
            continue

        # Check from word_senses, which 'pos' matches and modify that attribute 'affixed' as True or False

        for word_sense_index, curr_word_sense in enumerate(word_senses):
            if word_pos == curr_word_sense["pos"]:
                match_cql = generate_match_cql_string(rdr_condition, rdr_conclusion)
                index_cql = str(idx + 1)
                operation_cql = "+"

                # afx_modf == "OFF": mean there should'nt be affix , where there is
                # afx_modf == "ON": mean there should be affix, when there is'nt
                replace_cql = f'[senses[{word_sense_index}]["affixed"]={False}]'
                if afx_modf == "ON":
                    replace_cql = f'[senses[{word_sense_index}]["affixed"]={True}]'
                curr_new_cql_rule = "\t".join(
                    [match_cql, index_cql, operation_cql, replace_cql]
                )
                affix_cql_rules_collection += f"{curr_new_cql_rule}\n"

    return affix_cql_rules_collection


def generate_match_cql_string(rdr_condition, rdr_conclusion):
    # Generating match cql from rdr_condition and rdr conclusion
    match_cql = ""
    match_cql_inner_value = ""

    indices_for_rule_generation = [t[0] for t in rdr_conclusion]
    for i in indices_for_rule_generation:
        rdr_condition_attributes = list(rdr_condition[i].keys())
        no_of_attributes = len(rdr_condition_attributes)
        attr_counter = 0
        for rdr_condition_attr in rdr_condition_attributes:
            attr_counter += 1
            if rdr_condition_attr == "text":
                match_cql_inner_value += "{}={}".format(
                    rdr_condition_attr,
                    rdr_condition[i][rdr_condition_attr].replace("-", ""),
                )
            else:
                match_cql_inner_value += "{}={}".format(
                    rdr_condition_attr,
                    rdr_condition[i][rdr_condition_attr].replace("-", ""),
                )

            # IF there are more than one attribute, there should & sign btw then
            if attr_counter < no_of_attributes:
                match_cql_inner_value += "&"
    match_cql += f"[{match_cql_inner_value}]"
    return match_cql


if __name__ == "__main__":
    rdr_string = Path("src/data/TIB_train_maxmatched_tagged.txt.RDR").read_text(
        encoding="utf-8"
    )
    rdr_rules = split_merge_cql(rdr_string)
    print(rdr_rules)
