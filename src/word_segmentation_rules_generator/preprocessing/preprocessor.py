import re

from botok import TSEK


def replace_initial_patterns(file_string):
    # Some signs(i.e ?,+,- ) are presented in human annotated training files which needs to be edited
    # There are two different kind of TSEK, and here proper tsek been replaced
    initial_patterns = {"?": " ", "+": "", "-": " ", "[ ]+": " ", "༌":TSEK}
    modified_content = re.sub(
        "|".join(re.escape(key) for key in initial_patterns.keys()),
        lambda match: initial_patterns[match.group(0)],
        file_string,
    )
    return modified_content

def adjust_spaces(file_string):
    pattern = r"[ ]+"
    replacement = ' '
    modified_string = re.sub(pattern, replacement, file_string.strip())
    return modified_string

def adjust_spaces_for_non_affix(file_string):
    '''
    Sometimes there error in gold corpus i.e 
    string: ད གེ འོ་ བཀྲ་ཤིས་ ཤོག།
    Expected: དགེ འོ་ བཀྲ་ཤིས་ ཤོག།
    *Note that in དགེ འོ་, space before འོ་ is not closed,because this is an affix 
    '''
    pattern = r"([^་།_]) ([^ར ས འི འམ འང འོ འིའོ འིའམ འིའང འོའམ འོའང ། _])"
    replacement = r"\1\2"
    modified_string = re.sub(pattern, replacement, file_string)
    return modified_string

def file_2_botok(file_string):
    """
    input: string of a file before going under max match(botok)
    output/return: cleaned/preprocess string
    """

    modified_content = replace_initial_patterns(file_string)
    #making sure there only one space
    pattern = r"[ ]+"
    replacement = ' '
    modified_content = re.sub(pattern, replacement, modified_content)
    
    #Joining all the words, not leaving spaces unless its for SHAD
    patterns = {
        r'([^།]) ([^།])':r'\1\2', 
    }

    for pattern, replacement in patterns.items():
        modified_content = re.sub(pattern, replacement, modified_content)
    return modified_content


def gold_corpus_2_tagger(file_string):
    """
    input: string where words are separated with space by human annotators before going to tagger
    output/return: cleaned/preprocess string where words are still separated by space
    """
    modified_content = replace_initial_patterns(file_string)
    patterns = {
          '([^༅])།':r'\1 །', 
          '།\\s*།':'།_། ',
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
    gold_corpus_output = adjust_spaces(gold_corpus_output)
    gold_corpus_output = adjust_spaces_for_non_affix(gold_corpus_output)
    
    return gold_corpus_output

    
if __name__ == "__main__":
    pass
