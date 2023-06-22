import re

from botok import TSEK

from src.word_segmentation_rules_generator.preprocessing.preprocessor import adjust_spaces

from ..comparator.comparator import comparator

def split_by_TSEK(string_to_split):
    pattern = r"[་]+"  #Removing multiple TSEKs
    replacement = '་'
    string_to_split = re.sub(pattern, replacement, string_to_split)
    split_pattern = TSEK
    splited_list= re.split(split_pattern, string_to_split)
    if len(splited_list)==1:
        return splited_list
    for index, element in enumerate(splited_list):
        if element == '':
            splited_list[index-1] += TSEK
            break
        if index == len(splited_list)-1:
            break
        if splited_list[index+1] != '':
            splited_list[index] += TSEK
    
        
    splited_list = list(filter(None, splited_list))
    return splited_list

def split_list_with_TSEK(list_to_split):
    specific_character = TSEK
    split_list = []

    for element in list_to_split:
        if specific_character in element:
            insert_list = element.split(specific_character)
            split_list += insert_list
        else:
            split_list.append(element)
    split_list = list(filter(None, split_list))
    return split_list

# Building a tagged list for unmatched gold corpus syllables
def gold_corpus_tagger(gold_corpus_words, gold_index, gold_index_track):
    """
    Input: List of words of gold corpus
    Output: list of each syllable followed by the proper tag
    Eg:
    Input: ['ལ་', 'ལ་ལ་', 'ལ་', 'ལ་བ་'], gold_index=0, gold_index_track =3
    Output: ['ལ་', 'N', 'ལ་','N', 'ལ་', 'C', 'ལ་']

    N: means start of new word
    C: Continuation of the previous word
    A: New word but contains affix in gold corpus i.e ར|ས|འི|འམ|འང|འོ|འིའོ|འིའམ|འིའང|འོའམ|འོའང
    B: Continuation of the previous word but contains affix
    """
    gold_corpus_unmatched_word_list = gold_corpus_words[gold_index:gold_index_track]
    gold_corpus_syls_tagged = []

    for gold_corpus_unmatched_word in gold_corpus_unmatched_word_list:

        gold_corpus_unmatched_syls = split_by_TSEK(gold_corpus_unmatched_word)

        new_word = True
        for gold_corpus_unmatched_syl in gold_corpus_unmatched_syls:
            gold_corpus_syls_tagged.append(gold_corpus_unmatched_syl)
            if new_word:
                if '-' in gold_corpus_unmatched_syl:
                    gold_corpus_syls_tagged.append("A")
                else:
                    gold_corpus_syls_tagged.append("N")
                new_word = False
            else:
                if '-' in gold_corpus_unmatched_syl:
                    gold_corpus_syls_tagged.append("B")
                else:
                    gold_corpus_syls_tagged.append("C")
    return gold_corpus_syls_tagged


def tagger(file_string):
    # equal_number_of_syls, gold_corpus_output, botok_output = comparator(file_string)

    equal_number_of_syls, gold_corpus_output, botok_output = comparator(file_string)

    if equal_number_of_syls is False:
        return "ValueError: Output of gold corpus and botok output does not match. Something wrong in language structure."

    gold_corpus_output = adjust_spaces(gold_corpus_output)
    botok_output = adjust_spaces(botok_output)

    gold_corpus_words = gold_corpus_output.split()
    #Spliting on space and affixes, if max match has'nt done it
    # pattern = r"\s+|ར|ས|འི|འམ|འང|འོ|འིའོ|འིའམ|འིའང|འོའམ|འོའང"
    # botok_words = re.split(pattern, botok_output)
    botok_words = botok_output.split()
    botok_words_count = len(botok_words)
    gold_corpus_words_count = len(gold_corpus_words)

    gold_index = 0
    botok_index = 0
    tagged_content = ""
    while botok_index < botok_words_count and gold_index < gold_corpus_words_count:
        #Checking if the word is same, '_' is ignored because of possiblity of shads alignment
        condition1 = botok_words[botok_index].replace('_','') == gold_corpus_words[gold_index].replace('_','')

        # If the word matches perfectly in output of both botok and gold corpus
        if condition1:
            tagged_content += botok_words[botok_index] + "/P "
            gold_index += 1
            botok_index += 1
            continue

        gold_index_track = gold_index
        botok_index_track = botok_index

        # Find the occurence of the next perfect word that matches in output of both botok and gold corpus
        while (botok_index_track < botok_words_count) and (
            gold_index_track < gold_corpus_words_count
        ):

            condition_1 = (
                botok_words[botok_index_track].replace('_','') == gold_corpus_words[gold_index_track].replace('_','')
            )

            botok_unmatched_words = "".join(
                botok_words[botok_index : botok_index_track + 1]  # noqa
            )
            gold_corpus_unmatched_words = "".join(
                gold_corpus_words[gold_index : gold_index_track + 1]  # noqa
            )
            
            botok_unmatched_words = botok_unmatched_words.replace('_', '').replace('-','')
            gold_corpus_unmatched_words = gold_corpus_unmatched_words.replace('_', '').replace('-','')

            if condition_1 and (
                len(botok_unmatched_words) == len(gold_corpus_unmatched_words)
            ):
                break
            
            botok_unmatched_syls = split_list_with_TSEK(botok_words[botok_index : botok_index_track + 1])
            gold_corpus_unmatched_syls = split_list_with_TSEK(gold_corpus_words[gold_index : gold_index_track + 1])

            if len(botok_unmatched_syls) > len(gold_corpus_unmatched_syls):
                gold_index_track += 1
            elif len(botok_unmatched_syls) < len(gold_corpus_unmatched_syls):
                botok_index_track += 1
            else:
                gold_index_track += 1
                botok_index_track += 1

        # Calling function to get a tagged list for unmatched gold corpus syllables
        gold_corpus_syls_tagged = gold_corpus_tagger(
            gold_corpus_words, gold_index, gold_index_track
        )

        # Building tagged list for unmatched max match words based on gold corpus syllables
        botok_unmatched_word_list = botok_words[botok_index:botok_index_track]

        gold_corpus_syls_tagged_index = 0
        for botok_unmatched_word in botok_unmatched_word_list:
            botok_unmatched_syls = split_by_TSEK(botok_unmatched_word)
            botok_unmatched_syls_count = len(botok_unmatched_syls)
            botok_syls = ""
            botok_tags = ""
            
            botok_unmatched_syls_index = 0
            for i in range(
                gold_corpus_syls_tagged_index,
                (gold_corpus_syls_tagged_index + (2 * botok_unmatched_syls_count)),
                2,
            ):
                #botok_syls += gold_corpus_syls_tagged[i]
                botok_syls += botok_unmatched_syls[botok_unmatched_syls_index]
                botok_unmatched_syls_index += 1
                botok_tags += gold_corpus_syls_tagged[i + 1]

            tagged_content += botok_syls + "/" + botok_tags + " "
            gold_corpus_syls_tagged_index = gold_corpus_syls_tagged_index + (
                2 * botok_unmatched_syls_count
            )

        gold_index = gold_index_track
        botok_index = botok_index_track

    return tagged_content


if __name__ == "__main__":
    pass
