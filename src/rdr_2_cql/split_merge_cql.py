import sys
from pathlib import Path

# Add the root directory of your project to sys.path
root_path = (
    Path(__file__).resolve().parents[2]
)  # Adjust the number of parents as needed
sys.path.append(str(root_path))

from src.rdr_2_cql.rdr_2_replace_matcher import find_levels, find_rules  # noqa


def split_merge_cql(rdr_string):
    rdr_rules = find_rules(find_levels(rdr_string))
    for rdr_rule in rdr_rules:
        rdr_condition = rdr_rule["test"]
        rdr_conclusion = rdr_rule["ccl"][0][0][1]  # noqa

        # Checking for Tag intro (not an actual rule)
        # 	object.tag == "U" : object.conclusion = "U" (looks like this in the .RDR)
        if len(rdr_condition) == 1 and len(rdr_condition[0]) == 1:
            continue
    return rdr_rules


if __name__ == "__main__":
    rdr_string = Path("src/data/rdr_rules.txt").read_text(encoding="utf-8")
    rdr_rules = split_merge_cql(rdr_string)
