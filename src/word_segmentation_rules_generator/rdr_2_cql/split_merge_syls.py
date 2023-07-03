import os

from src.word_segmentation_rules_generator.tagger.tagger import split_by_TSEK


def split_merge_syls(tagged_file="TIB_train_maxmatched.txt.TAGGED"):
    """
    Input: file that is tagged by rdr rules
    Output:
    """
    current_dir = os.path.dirname(__file__)
    relative_path = "../data/" + tagged_file
    file_path = os.path.join(current_dir, relative_path)

    file = open(file_path, encoding="utf-8")
    contents = file.read()
    words_list = contents.split()
    word_tag_list = []
    counter = 0
    for word in words_list:
        counter += 1
        if counter > 100:
            break
        word_tag_splited = word.split("/")
        if word_tag_splited[1] == "P":
            word_tag_list.append(word_tag_splited)
        else:
            syls_list = split_by_TSEK(word_tag_splited[0])
            if len(syls_list) != len(word_tag_splited[1]):
                print(
                    "Error in the resulted tagged file, number of syllables is not equal to number of tags."
                )
            for i in range(len(syls_list)):
                word_tag_list.append([syls_list[i], word_tag_splited[1][i]])
    print(word_tag_list)
