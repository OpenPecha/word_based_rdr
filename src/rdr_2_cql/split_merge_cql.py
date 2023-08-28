from pathlib import Path

from rdr_2_replace_matcher import find_levels, find_rules


def split_merge_cql(rdr_string):
    rdr_format = find_rules(find_levels(rdr_string))
    return rdr_format


if __name__ == "__main__":
    rdr_string = Path("src/data/rdr_rules.txt").read_text(encoding="utf-8")
    result = split_merge_cql(rdr_string)
    for r in result:
        print(r["test"])
