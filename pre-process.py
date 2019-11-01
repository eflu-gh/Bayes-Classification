import os
import json
import sys


def separate_punctuation(text):
    txt = ""
    for character in range(len(text)):
        if text[character] in punctuation:
            if character == 0:
                txt = text[character]
                continue
            if text[character - 1] == " ":
                txt = txt + text[character]
                continue
            if text[character - 1] in punctuation:
                txt = txt + " " + text[character]
                continue
            else:
                txt = txt + " " + text[character]
                continue
        else:
            if text[character] == " ":
                txt = txt + text[character]
                continue
            if text[character - 1] in punctuation:
                txt = txt + " " + text[character]
            else:
                txt = txt + text[character]
    return txt.lower()


def createVocabulary(directory):
    vocab = []
    list = directory.split('/')
    namedir = list[0]
    for label in os.listdir(directory):  # root directory
        folder = os.path.join(directory, label)  # test and train directories
        if os.path.isdir(folder):
            for file in os.listdir(folder):  # for each file in train or test directory
                if file.endswith(".txt"):
                    file = open(os.path.join(folder, file), "r", encoding="utf8")  # open and read each file
                    text_in_document = file.read()
                    text_processed_in_document = separate_punctuation(text_in_document)
                    words = text_processed_in_document.split()
                    for word in words:
                        if word not in punctuation and word not in vocab:
                            vocab.append(word.rstrip())
                    file.close()
    file = open(namedir + '/imdb.vocab', "w", encoding="utf8")
    for line in range(len(vocab)):
        if line == 0:
            file.write(vocab[line])
        else:
            file.write('\n' + vocab[line])
    file.close()
    return vocab


# Get the number of times where a word appears in a given file
def getFrequenciesPerWord(text, vocabulary):
    dictionary = {}
    words = text.split()
    for keyword in words:
        if keyword not in punctuation and keyword in vocabulary:
            if keyword in dictionary:
                dictionary[keyword] += 1  # There is already a keyword
            else:
                dictionary[keyword] = 1  # keyword is new
    return dictionary


# It creates a vector for each file or processed text.
def create_vector_bag_of_words(text_processed_in_document, label, vocabulary):
    vector = {}
    vector = getFrequenciesPerWord(text_processed_in_document, vocabulary)
    return vector


def create_file(file_name, list_of_dictionaries):
    file = open(file_name, "w")
    i = 0
    for line in list_of_dictionaries:
        if i == 0:
            file.write(json.dumps(line))  # dumps is used to hangle strings.
        else:
            file.write('\n' + json.dumps(line))  # dumps is used to hangle strings.
        i = 1
    print("Bag of words created: " + file_name)
    file.close()


def pre_processing(directory, vocabulary):
    list_of_dictionaries = []
    try:
        for label in os.listdir(directory):  # root directory
            folder = os.path.join(directory, label)  # test and train directories
            if os.path.isdir(folder):
                for file in os.listdir(folder):  # for each file in train or test directory
                    if file.endswith(".txt"):
                        file = open(os.path.join(folder, file), "r", encoding="utf8")  # open and read each file
                        text_in_document = file.read()
                        text_processed_in_document = separate_punctuation(text_in_document)
                        # dir is treated as the label for each sentiment and vector is the dictionary for each text.
                        vector = create_vector_bag_of_words(text_processed_in_document, label, vocabulary)
                        # create vectors for each file and then write it into the train file BOW - vector
                        list_of_dictionaries.append({label: vector})
                        file.close()
        list = directory.split('/')
        dir_name = list[0]
        file_name = dir_name + "/" + list[1] + "BOW" + ".txt"
        create_file(file_name, list_of_dictionaries)

    except FileNotFoundError:
        print('Directory does not exist.')
        exit()


def init_pre_processing():
    vocabulary = []
    try:
        print("Insert the directory name to pre-process: ")
        directory =  input()
        print("Indicate what do you want to train (train/test partition): ")
        option = input()
        path = directory + "/" + option

        if os.path.exists(directory + "/imdb.vocab") is False:
            vocabulary = createVocabulary(path)
        else:
            file = open(directory + '/imdb.vocab', encoding="utf8")
            for line in file.readlines():
                vocabulary.append(line.rstrip())
            file.close()
        print("Pre-processing corpus in " + path)
        pre_processing(path, vocabulary)

    except FileNotFoundError:
        print('Directory does not exist.')
        exit()

punctuation = [',', ';', ':', '.', '!', '?', '`', '~', '_', '+', '*', '@', '$', '%', '&', '#', '=', '"', '^', '{', '}',
                   '[', ']', '|', '\\', '<', '>', '(', ')', '/']

init_pre_processing ()