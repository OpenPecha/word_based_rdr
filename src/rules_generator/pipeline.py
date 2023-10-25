import re
from pathlib import Path

from rules_generator.rdr_to_cql import convert_rdr_to_cql
from rules_generator.tagger import tagger
from rules_generator.train_tag_rdr import train_with_external_rdr


def convert_tags_to_perfect_tag(text: str) -> str:
    """
    Input: Text with tags
    Output: Text with perfect tags
    Eg: 'ལ་ལ་/BB ལ་ལ་/BB ལ་བ་/U ཡོད་/U' -> 'ལ་ལ་/U ལ་ལ་/U ལ་བ་/U ཡོད་/U'
    """

    pattern = r"/[BIUXY]+"
    replacement = r"/U"
    return re.sub(pattern, replacement, text)


def pipeline(gold_corpus, num_parts):
    tagger_output = tagger(gold_corpus)
    DATA_DIR = Path(__file__).resolve().parent / "data"

    with open(DATA_DIR / "gold_corpus.TAGGED", "w", encoding="utf-8") as fileout:
        fileout.write(tagger_output)

    print("Tagging done....")

    # Split the tagger_output into parts based on newlines
    all_lines = tagger_output.split("\n")
    lines_per_part = len(all_lines) // num_parts
    parts = []

    for i in range(num_parts):
        # For the last part, we take all the remaining lines
        if i == num_parts - 1:
            parts.append("\n".join(all_lines[i * lines_per_part :]))  # noqa
        else:
            parts.append(
                "\n".join(
                    all_lines[i * lines_per_part : (i + 1) * lines_per_part]  # noqa
                )
            )

    rdr_rules_combined = ""  # This will store the combined rdr rules

    # Process each part
    for i, current_part in enumerate(parts, 1):
        external_tagger_output = convert_tags_to_perfect_tag(current_part)
        rdr_rules = train_with_external_rdr(
            current_part, external_tagger_output, (3, 2)
        )

        # Append the rdr_rules from the current part to the combined rules
        if rdr_rules is not None:
            rdr_rules_combined += rdr_rules
        print(f"RDR rules done for part {i}....")

    # Save the combined RDR rules to the file
    with open(DATA_DIR / "gold_corpus.RDR", "w", encoding="utf-8") as fileout:
        fileout.write(rdr_rules_combined)

    print("All RDR rules done....")

    # Convert the combined RDR rules to CQL rules and save them
    cql_rules = convert_rdr_to_cql(rdr_rules_combined)
    with open(DATA_DIR / "gold_corpus.tsv", "w", encoding="utf-8") as fileout:
        fileout.write(cql_rules)

    print("CQL rules done....")

    return cql_rules


if __name__ == "__main__":
    DATA_DIR = Path(__file__).resolve().parent / "data"
    gold_corpus = Path(DATA_DIR / "TIB_train.txt").read_text(encoding="utf-8")
    cql_rules = pipeline(gold_corpus, 5)
    print(cql_rules)
