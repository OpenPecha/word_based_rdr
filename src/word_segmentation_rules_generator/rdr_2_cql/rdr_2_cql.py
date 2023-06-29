import os

from pybo.rdr.rdr_2_replace_matcher import rdr_2_replace_matcher


def rdr_2_cql(rdr_rules_file="TIB_train_maxmatched_tagged.txt.RDR"):
    current_dir = os.path.dirname(__file__)
    relative_path = "../resources/" + rdr_rules_file
    file_path = os.path.join(current_dir, relative_path)

    with open(file_path, encoding="utf-8") as file:
        rdr_rules = file.read()  # Read the entire file content
        cql_rules = rdr_2_replace_matcher(rdr_rules)
        # in the code rdr_2_replace_matcher, there been done pos but here we will need word tag
        cql_rules = cql_rules.replace("pos", "word_tag")
        current_dir = os.path.dirname(__file__)
        cql_file_relative_path = "../resources/" + "TIB_train_CQL_rules.txt"
        cql_file_path = os.path.join(current_dir, cql_file_relative_path)
        with open(cql_file_path, "w", encoding="utf-8") as file:
            file.write(cql_rules)  # Write content to the file
