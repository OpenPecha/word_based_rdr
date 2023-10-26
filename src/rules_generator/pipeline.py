import re
from pathlib import Path

from botok import WordTokenizer

from rules_generator.annotation_transfer import newline_annotations_transfer
from rules_generator.data_processor import transform_gold_corpus_for_tagging
from rules_generator.rdr_to_cql import convert_rdr_to_cql
from rules_generator.tagger import tagger
from rules_generator.tokenizer_pipeline import botok_word_tokenizer_pipeline
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
    DATA_DIR = Path(__file__).resolve().parent / "data"

    # Initially, split the gold_corpus into parts based on newlines
    all_lines = gold_corpus.split("\n")
    lines_per_part = len(all_lines) // num_parts

    rdr_rules_combined = ""  # This will store the combined rdr rules

    # loading outside the loop to avoid loading it again and again
    wt = WordTokenizer()
    # Process each part
    for i in range(num_parts):
        print(f"Processing part [{i + 1}/{num_parts}]...")

        # Calculate the starting and ending index for each part
        start_index = i * lines_per_part
        if i == num_parts - 1:
            end_index = None  # Take all the remaining lines in the last part
        else:
            end_index = (i + 1) * lines_per_part

        # Segment of the corpus that we will work with in this iteration
        current_corpus = "\n".join(all_lines[start_index:end_index])

        # Tokenization and preparation for the current part of the gold corpus
        tokenized_output = botok_word_tokenizer_pipeline(wt, current_corpus)

        gold_corpus_cleaned = transform_gold_corpus_for_tagging(current_corpus)
        gold_corpus_cleaned = newline_annotations_transfer(
            tokenized_output, gold_corpus_cleaned
        )

        # Tag the current part of the corpus
        tagger_output = tagger(gold_corpus_cleaned, tokenized_output)

        # Additional processing (e.g., conversion, training) on the tagger output
        external_tagger_output = convert_tags_to_perfect_tag(tagger_output)
        rdr_rules = train_with_external_rdr(
            tagger_output, external_tagger_output, (3, 2)
        )

        # Append the rdr_rules from the current part to the combined rules
        if rdr_rules is not None:
            rdr_rules_combined += rdr_rules

        print(f"RDR rules done for part {i + 1}....")

    # After processing all parts, we handle the combined results

    # Save the combined RDR rules to a file
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
    gold_corpus = Path(DATA_DIR / "TIB_demo.txt").read_text(encoding="utf-8")
    cql_rules = pipeline(gold_corpus, 1)
    print(cql_rules)
