from pathlib import Path

from rules_generator.data_processor import (
    prepare_gold_corpus_for_tokenizer,
    remove_extra_spaces,
    transform_gold_corpus_for_tagging,
)
from rules_generator.Utility.regex_replacer import replace_with_regex


def botok_word_tokenizer_pipeline(wt, gold_corpus: str) -> str:
    """
    input: string of a file before going under max match(botok)
    output/return: cleaned/preprocessed string and word segmented
    """
    lines = gold_corpus.splitlines()
    tokenized_lines = []
    counter = 1
    for line in lines:
        print(f"Processing line [{counter}/{len(lines)}]")
        counter += 1
        preprocessed_text = prepare_gold_corpus_for_tokenizer(line)
        tokens = wt.tokenize(preprocessed_text, split_affixes=True)
        tokenized_text = " ".join(token.text for token in tokens)
        tokenized_text = transform_gold_corpus_for_tagging(tokenized_text)
        tokenized_text = remove_extra_spaces(tokenized_text)
        tokenized_text = add_hyphens_to_affixes(tokenized_text)
        tokenized_lines.append(tokenized_text)

    tokenized_corpus = "\n".join(tokenized_lines)
    return tokenized_corpus


def add_hyphens_to_affixes(text: str) -> str:
    """
    Input: རིན་པོ་ཆེའི་, tokenized output: རིན་པོ་ཆེ འི་, after replacement རིན་པོ་ཆེ-འི་
    """
    pattern = r"((?![་།_༠༡༢༣༤༥༦༧༨༩])[\u0F00-\u0FFF]) (ར|ས|འི|འམ|འང|འོ|འིའོ|འིའམ|འིའང|འོའམ|འོའང)"
    replacement = r"\1-\2"
    text = replace_with_regex({pattern: replacement}, text)
    return text


if __name__ == "__main__":
    DATA_DIR = Path(__file__).resolve().parent / "data"
    gold_corpus = Path(DATA_DIR / "gold_corpus.txt").read_text(encoding="utf-8")
