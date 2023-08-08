import os

# from pybo.rdr.rdr_2_replace_matcher import rdr_2_replace_matcher
from .rdr_2_replace_matcher import rdr_2_replace_matcher


def rdr_2_cql_string(rdr_rules_string):
    cql_rules = rdr_2_replace_matcher(rdr_rules_string)
    return cql_rules


def rdr_2_cql_file(
    rdr_rules_file="TIB_train_maxmatched_tagged.txt.RDR",
    new_cql_file_name="TIB_train_CQL_rules_temp.txt",
):
    current_dir = os.path.dirname(__file__)
    relative_path = "../resources/" + rdr_rules_file
    file_path = os.path.join(current_dir, relative_path)

    with open(file_path, encoding="utf-8") as file:
        rdr_rules = file.read()  # Read the entire file content
        cql_rules = rdr_2_cql_string(rdr_rules)
        current_dir = os.path.dirname(__file__)
        cql_file_relative_path = "../resources/" + new_cql_file_name
        cql_file_path = os.path.join(current_dir, cql_file_relative_path)
        with open(cql_file_path, "w", encoding="utf-8") as file:
            file.write(cql_rules)  # Write content to the file


def append_new_cql_rules_to_main(new_cql_rules, destination_file):
    """
    Used to append the replace cql rules of minimum cases to the main file
    """
    current_dir = os.path.dirname(__file__)

    destination_relative_path = "../resources/" + destination_file
    destination_file_path = os.path.join(current_dir, destination_relative_path)

    try:

        lines_to_append = new_cql_rules.splitlines()
        with open(destination_file_path, "a") as destination:
            for line in lines_to_append:
                destination.write(line)
        print("new cql rules successfully appended to the destination file.")
    except FileNotFoundError:
        print("One of the files does not exist.")
    except Exception as e:
        print("An error occurred:", str(e))
