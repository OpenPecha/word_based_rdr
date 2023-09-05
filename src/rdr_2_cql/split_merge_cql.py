import sys
from pathlib import Path

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
    rdr_string = Path("src/data/TIB_demo.RDR").read_text(encoding="utf-8")
    rdr_rules = split_merge_cql(rdr_string)
