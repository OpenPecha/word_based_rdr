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

        need_affix_rule_generation = False
        # if there is a need for affix modification, this will store index, and operation in tuple
        affix_modification = []
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
            # new rule generation
            # rdr condition and rdr conclusion will be updated
            new_cql_affix_rule, rdr_condition, rdr_conclusion = generate_affix_rule(
                rdr_condition, rdr_conclusion, affix_modification
            )
            cql_rules_collection += f"{new_cql_affix_rule}\n"

        # if the rule is not proper, jumps to next rule
        if is_unnecessary_rule:
            continue

        need_split_rule_generation = False
        # if there is a need for split modification, this will store index, and syllable index a in tuple
        split_modification = []
        # Checking for split rule generation
        for rdr_conclusion_tuple in rdr_conclusion:
            rdr_conclusion_tag = rdr_conclusion_tuple[1]

            # Getting tag of each syls for checking if split rules generation is needed
            # rdr_condition_syls = ['ལ་', 'ལ་'],
            # rdr_conclusion_tag_list = ['B', 'B']
            rdr_condition_text = rdr_condition[rdr_conclusion_tuple[0]]["text"]
            rdr_condition_syls = split_by_TSEK(rdr_condition_text)

            rdr_conclusion_tag_list = list(rdr_conclusion_tag)

            # Cleaning empty elements after conversion from word to syls
            rdr_condition_syls = [x for x in rdr_condition_syls if x != "" and x != '"']
            rdr_conclusion_tag_list = [
                x for x in rdr_conclusion_tag_list if x != "" and x != '"'
            ]

            for idx_for_split, curr_syl in enumerate(rdr_condition_syls):
                if idx_for_split != 0 and rdr_conclusion_tag_list[idx_for_split] in [
                    "B",
                    "X",
                ]:
                    need_split_rule_generation = True
                    split_modification.append((rdr_conclusion_tuple[0], idx_for_split))
        if need_split_rule_generation:
            new_cql_split_rule, rdr_condition, rdr_conclusion = generate_split_rule(
                rdr_condition, rdr_conclusion, split_modification
            )
            cql_rules_collection += f"{new_cql_split_rule}"

        need_merge_rule_generation = False
        # if there is a need for merge modification, this will store index, and syllable index a in tuple
        merge_modification = []
        # Checking for merge rule generation
        is_first_tuple = True

        for rdr_conclusion_tuple in rdr_conclusion:
            if is_first_tuple:
                is_first_tuple = False

                continue
            rdr_conclusion_tag = rdr_conclusion_tuple[1]
            rdr_conclusion_tag_list = list(rdr_conclusion_tag)

            # Cleaning empty elements after conversion from word to syls
            rdr_conclusion_tag_list = [
                x for x in rdr_conclusion_tag_list if x != "" and x != '"'
            ]

            if rdr_conclusion_tag_list[0] in ["I", "Y"]:
                # Check if the prev index has a word to merge with
                index_to_check = rdr_conclusion_tuple[0] - 1
                is_index_in_rdr_condition = any(
                    index_to_check == key for key in list(rdr_condition.keys())
                )
                is_text_in_prev_index_condition = False
                if is_index_in_rdr_condition:
                    is_text_in_prev_index_condition = any(
                        "text" in key
                        for key in list(rdr_condition[index_to_check].keys())
                    )
                if is_text_in_prev_index_condition:
                    need_merge_rule_generation = True
                    merge_modification.append(rdr_conclusion_tuple[0])

        if need_merge_rule_generation:
            new_cql_merge_rule = generate_merge_rule(
                rdr_condition, rdr_conclusion, merge_modification
            )
            cql_rules_collection += f"{new_cql_merge_rule}"

    return cql_rules_collection


def generate_merge_rule(rdr_condition, rdr_conclusion, merge_modification):
    # Collecting all the cql rule string

    merge_cql_rules_collection = ""
    for i, word_index in enumerate(merge_modification):
        match_cql = generate_match_cql_string(rdr_condition, rdr_conclusion)
        # We are substracting i from word_index because with each iteration and merging,
        # the index of the word get reduced by 1
        # We can consider this as modifying the merge_modification list
        index_cql = str(word_index - i)
        operation_cql = "+"

        merge_index = word_index - 1 - i
        left_merge_word = rdr_condition[merge_index]["text"]
        right_merge_word = rdr_condition[merge_index + 1]["text"]
        new_merged_word = left_merge_word + right_merge_word
        new_merged_word = new_merged_word.replace('"', "").replace('"', "")
        new_merged_word_POS = get_POS(new_merged_word)
        if new_merged_word_POS in [NO_POS, empty_POS]:
            replace_cql = "[]"
        else:
            replace_cql = f"[pos='{new_merged_word_POS}']"
        curr_new_cql_rule = "\t".join(
            [match_cql, index_cql, operation_cql, replace_cql]
        )

        merge_cql_rules_collection += curr_new_cql_rule + "\n"
        # modifying rdr_condition, rdr_conclusion
        # 1.modifying rdr_condition
        merge_index = next(
            i for i, item in enumerate(rdr_conclusion) if item[0] == word_index
        )
        # Shifting the values to the left
        rdr_conclusion[merge_index + 2 :] = [  # noqa
            (i - 1, tag) for i, tag in rdr_conclusion[merge_index + 2 :]  # noqa
        ]
        # Updating the merged tag in rdr conclusion
        rdr_conclusion[merge_index : merge_index + 2] = [  # noqa
            (merge_index, new_merged_word)
        ]

        # 2. modifying rdr_condition
        new_dict = {}
        rdr_condition_keys = list(rdr_condition.keys())
        rdr_condition_keys.sort()

        for key in rdr_condition_keys:
            if key + 1 < merge_index:
                new_dict[key] = rdr_condition[key]
            # if the key == word_index, we need to insert two dictionary (after split, two words comes)
            elif key + 1 == merge_index:
                new_dict[key] = {"text": new_merged_word}
            elif key == merge_index:
                continue
            else:
                # if key > word_index, we need to add 0 or 1 to the key, depending on add_or_not
                new_dict[key - 1] = rdr_condition[key]
        rdr_condition = new_dict

    return merge_cql_rules_collection


def generate_split_rule(rdr_condition, rdr_conclusion, split_modification):
    # Collecting all the cql rule string
    # split_modification is list of tuples, storing index and syllable index of the word to split

    split_cql_rules_collection = ""
    for word_index, syl_index in split_modification:
        match_cql = generate_match_cql_string(rdr_condition, rdr_conclusion)

        # Getting value for syls and tag of word index
        rdr_condition_text = rdr_condition[word_index]["text"]
        rdr_condition_syls = split_by_TSEK(rdr_condition_text)

        split_index = next(
            i for i, item in enumerate(rdr_conclusion) if item[0] == word_index
        )
        rdr_conclusion_tag = rdr_conclusion[split_index][1]
        rdr_conclusion_tag_list = list(rdr_conclusion_tag)

        # Cleaning empty elements after conversion from word to syls
        rdr_condition_syls = [x for x in rdr_condition_syls if x != "" and x != '"']
        rdr_conclusion_tag_list = [
            x for x in rdr_conclusion_tag_list if x != "" and x != '"'
        ]

        # Removing double and single quotes from the syls
        rdr_condition_syls = [
            text.replace('"', "").replace('"', "") for text in rdr_condition_syls
        ]
        rdr_conclusion_tag_list = [
            text.replace('"', "").replace('"', "") for text in rdr_conclusion_tag_list
        ]

        char_index = len("".join(rdr_condition_syls[:syl_index]))
        index_cql = f"{word_index+1}-{char_index}"
        operation_cql = "::"

        left_splited_word = "".join(rdr_condition_syls[:syl_index])
        left_splited_word_POS = get_POS(left_splited_word)
        right_splited_word = "".join(rdr_condition_syls[syl_index:])
        right_splited_word_POS = get_POS(right_splited_word)

        replace_cql = ""
        if left_splited_word_POS in [NO_POS, empty_POS] and right_splited_word_POS in [
            NO_POS,
            empty_POS,
        ]:
            replace_cql = "[][]"
        elif left_splited_word_POS in [NO_POS, empty_POS]:
            replace_cql = f"[][pos={right_splited_word_POS}]"
        elif right_splited_word_POS in [NO_POS, empty_POS]:
            replace_cql = f"[pos={left_splited_word_POS}][]"
        else:
            replace_cql = f"[pos={left_splited_word_POS}][pos={right_splited_word_POS}]"

        curr_new_cql_rule = "\t".join(
            [match_cql, index_cql, operation_cql, replace_cql]
        )
        split_cql_rules_collection += curr_new_cql_rule + "\n"
        # modifying the rdr_condition, rdr_conclusion and split_modification
        # 1.modifying split_modification
        found = any(
            split_modification_tuple[0] == word_index + 1
            for split_modification_tuple in split_modification
        )
        add_or_not = 1 if found else 0
        split_modification[split_index + 1 :] = [  # noqa
            (i + add_or_not, syl_index)
            for i, syl_index in split_modification[split_index + 1 :]  # noqa
        ]
        # 2.modifying rdr_conclusion
        left_splited_tag = "".join(rdr_conclusion_tag_list[:syl_index])
        right_splited_tag = "".join(rdr_conclusion_tag_list[syl_index:])
        # add_or_not, if word_index+1 is present in rdr_conclusion, then add 1 to the index
        found = any(
            rdr_conclusion_tuple[0] == word_index + 1
            for rdr_conclusion_tuple in rdr_conclusion
        )
        add_or_not = 1 if found else 0
        # Shifting the index value of tuple elements right to the split index
        rdr_conclusion[split_index + 1 :] = [  # noqa
            (i + add_or_not, tag)
            for i, tag in rdr_conclusion[split_index + 1 :]  # noqa
        ]
        # Now inserting the new splitted index tag tuple
        rdr_conclusion[split_index : split_index + 1] = [  # noqa
            (word_index, left_splited_tag),
            (word_index + 1, right_splited_tag),
        ]

        # 3. modifying rdr_condition
        new_dict = {}
        rdr_condition_keys = list(rdr_condition.keys())
        rdr_condition_keys.sort()
        add_or_not = 0
        # Checking if word_index+1 is present in keys or not
        # EG of rdr_condition and word_index = 0
        # {0: {'text': '"ལ་ལ་"'}, 1: {'text': '"ལ་ལ་"'}} <- add_or_not = 1
        # {0: {'text': '"ལ་ལ་"'}, 2: {'text': '"ལ་ལ་"'}} <- add_or_not = 0
        # In second example, after splitting the word_index=0, doesnt effect the rest of the keys
        if word_index + 1 in rdr_condition_keys:
            add_or_not = 1
        for key in rdr_condition_keys:
            if key < word_index:
                new_dict[key] = rdr_condition[key]
            # if the key == word_index, we need to insert two dictionary (after split, two words comes)
            elif key == word_index:
                new_dict[key] = {"text": left_splited_word}
                new_dict[key + 1] = {"text": right_splited_word}
            else:
                # if key > word_index, we need to add 0 or 1 to the key, depending on add_or_not
                new_dict[key + add_or_not] = rdr_condition[key]
        rdr_condition = new_dict

    return split_cql_rules_collection, rdr_condition, rdr_conclusion


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
                affix_cql_rules_collection += curr_new_cql_rule + "\n"

    return affix_cql_rules_collection


def generate_match_cql_string(rdr_condition, rdr_conclusion):
    # Generating match cql from rdr_condition and rdr conclusion
    match_cql = ""

    indices_for_rule_generation = [t[0] for t in rdr_conclusion]
    for i, index in enumerate(indices_for_rule_generation):
        rdr_condition_attributes = list(rdr_condition[index].keys())
        no_of_attributes = len(rdr_condition_attributes)
        attr_counter = 0
        match_cql_inner_value = ""
        for rdr_condition_attr in rdr_condition_attributes:
            attr_counter += 1
            if rdr_condition_attr == "text":
                match_cql_inner_value += '"{}"'.format(
                    rdr_condition[index][rdr_condition_attr]
                    .replace("-", "")
                    .replace('"', "")
                    .replace("'", ""),
                )
            else:
                match_cql_inner_value += '{}="{}"'.format(
                    rdr_condition_attr,
                    rdr_condition[index][rdr_condition_attr]
                    .replace('"', "")
                    .replace("'", ""),
                )

            # IF there are more than one attribute, there should & sign btw then
            if attr_counter < no_of_attributes:
                match_cql_inner_value += "&"
        match_cql += f"[{match_cql_inner_value}]"
        if i < len(indices_for_rule_generation) - 1:
            match_cql += " "

    return match_cql


if __name__ == "__main__":
    rdr_string = Path("src/data/TIB_demo.RDR").read_text(encoding="utf-8")
    cql_rules = split_merge_cql(rdr_string)
    with open("src/data/TIB_demo.tsv", "w", encoding="utf-8") as tsvfile:
        tsvfile.write(cql_rules)
