import re

from botok import Text 


def replace_initial_patterns(file_string):
    # Some signs(i.e ?,+,- ) are presented in human annotated training files which needs to be edited
    initial_patterns = {"?": " ", "+": "", "-": "", "[ ]+": " "}
    modified_content = re.sub(
        "|".join(re.escape(key) for key in initial_patterns.keys()),
        lambda match: initial_patterns[match.group(0)],
        file_string,
    )
    return modified_content

def tokenize_chunks_cleanup(file_string):
    patterns = {r"([^།_]) ([^།_])": r"\1\2", r"([^།])_ ": r"\1 "}
    modified_content = file_string
    for pattern, replacement in patterns.items():
        modified_content = re.sub(pattern, replacement, modified_content)
    return modified_content

def file_2_botok(file_string):
    """
    input: string of a file before going under max match(botok)
    output/return: cleaned/preprocess string
    """
    modified_content = replace_initial_patterns(file_string)
    t = Text(modified_content)
    preprocessed_string = t.tokenize_chunks_plaintext
    return preprocessed_string


def gold_corpus_2_tagger(file_string):
    """
    input: string where words are separated with space by human annotators before going to tagger
    output/return: cleaned/preprocess string where words are still separated by space
    """
    modified_content = replace_initial_patterns(file_string)
    patterns = {
        #  '(་|༌)':r'\1 ', #Full stop (2 different kind)
          '([^༅])།':r'\1 །', 
          '།\s*།':'།_། ',
          '([^_༅])། ': r'\1 །_ ',# དུ། -> དུ །_ 
          ' །([^_])': r' །_ \1', # །བསྲེགས ->  །_ བསྲེགས་
          '([^།་༌_ ]) ': r'\1 ',  # Putting full stop དུ། -> དུ་ །_
    }
    for pattern, replacement in patterns.items():
        modified_content = re.sub(pattern, replacement, modified_content)
    #making sure there only one space
    pattern = r"[ ]+"
    replacement = ' '
    gold_corpus_output = re.sub(pattern, replacement, modified_content)
    

    return gold_corpus_output

    
if __name__ == "__main__":
    pass
