import json
import os
import math


def create_file_parameters(name, prior_probability, parameters_probability):
    file = open(directory + '/' + name, "w", encoding="utf8")
    i = 0
    file.write("Prior probability of each class: " + '\n')
    for label in prior_probability:
        file.write("P(" + label + ") = " + str(prior_probability[label]) + '\n')
    file.write('\n'"Probability of each feature in vocabulary given a class: " + '\n')
    for label, items in parameters_probability.items():
        for keyword in items:
            if i == 0:
                file.write(("P(" + keyword + " | " + label + ") = " + str(parameters_probability[label][keyword])))
            else:
                file.write(
                    '\n' + ("P(" + keyword + " | " + label + ") = " + str(parameters_probability[label][keyword])))
            i = 1;
    file.close()


def create_file_prediction(name, actual, production):
    file = open(directory + '/' + name, "w", encoding="utf8")
    i = 0
    count = 0
    total = 0
    file.write("Test Document" + "\t\t" + "Actual Label" + "\t\t" + "Prediction Label"'\t\t' + '\n')
    for key in range(len(actual)):
        file.write("Document " + str(i) + "\t\t\t\t" + str(actual[key]) + "\t\t\t\t" + str(production[key]) + '\n')
        i = i + 1
        if actual[key] == production[key]:
            count = count + 1
        total = total + 1
    file.write("\nTested documents: " + str(total) +
               " Equal document prediction: " + str(count) +
               " Different document prediction: " + str(total - count) +
               " Overall accuracy: " + str(((count / total) * 100)) + "%")
    file.close()


def get_Vocabulary():
    try:
        vocabulary = []
        file = open(directory + '/imdb.vocab', encoding="utf8")
        for line in file.readlines():
            vocabulary.append(line.rstrip())
        file.close()
    except FileNotFoundError:
        print("File imdb.vocab not found.")
        exit()
    return vocabulary


def total_number_documents():
    total_doc_per_class = {}
    total_documents = 0
    count_doc_per_class = 0
    classes = []
    try:
        for label in os.listdir(path):  # root directory
            folder = os.path.join(path, label)  # test and train directories
            classes.append(label)
            if os.path.isdir(folder):
                for file in os.listdir(folder):  # for each file in train or test directory
                    if file.endswith(".txt"):
                        total_documents = total_documents + 1
                    count_doc_per_class = count_doc_per_class + 1
            total_doc_per_class[label] = count_doc_per_class
            count_doc_per_class = 0
    except FileNotFoundError:
        print("Directory not found. " + path)
        exit()
    return total_documents, total_doc_per_class, classes


def upload_train_data(t_file, classes):
    try:
        data = []
        file = open(t_file, "r")
        for line in file.readlines():
            data.append(json.loads(line))

        bow = {}
        for label in classes:
            bow[label] = {}  # Creating a dictionary of bag of words for each label.

        for list in data:
            for label, items in list.items():
                for keyword in items:
                    if keyword in bow[label]:
                        bow[label][keyword] = list[label][keyword] + bow[label][keyword]
                    else:
                        bow[label][keyword] = list[label][keyword]  # value of label keyword
    except FileNotFoundError:
        print("File " + t_file + ' not found.')
        exit()
    return bow


def upload_test_data(t_file):
    try:
        data = []
        file = open(t_file, "r")
        for line in file.readlines():
            data.append(json.loads(line))
        file.close()
    except FileNotFoundError:
        print("File " + t_file + ' not found.')
        exit()
    return data


def get_count_words_per_class(bow):
    words_per_class = {}
    for label, items in bow.items():
        words_per_class[label] = 0
        for keyword in items:
            words_per_class[label] = words_per_class[label] + items[keyword]
    return words_per_class


def y_arg_max(probabilities):
    keys = list(probabilities.keys())  # Converting the keys to list
    values = list(probabilities.values())  # Converting the values to list
    max_arg = max(values)  # Getting the maximun
    index = values.index(max_arg)  # Getting the index where the maximun values is located
    return keys[index]  # Getting the class given the index


def NB_classifier(bow, classes, total_doc_per_class, total_documents):
    vocabulary = []
    prior_probability = {}
    parameters_probability = {}
    vocabulary = get_Vocabulary()
    words_per_class = get_count_words_per_class(bow)
    # Calculating the prior probability for each class.
    for label in classes:
        prior_probability[label] = math.log2(total_doc_per_class[label] / total_documents)

    lenVocab = len(vocabulary)

    for label in classes:
        parameters_probability[label] = {}
        for word_vocab in vocabulary:
            if word_vocab in bow[label]:
                parameters_probability[label][word_vocab] = math.log2(
                    (bow[label][word_vocab] + 1) / (words_per_class[label] + lenVocab))
            else:
                parameters_probability[label][word_vocab] = math.log2(1 / (words_per_class[label] + lenVocab))
    return prior_probability, parameters_probability, vocabulary


def NB_test(doc, prior_probability, parameters_probability, classes):
    sum_log_probabilities = {}
    probability = 0
    for c in classes:
        for label, items in doc.items():
            for keyword in items:
                # parameters_probability[c][keyword] * items[keyword] it is multiplied by items[keyword] because the
                # testBOW.txt file has been pre-processed and it does not take account values that are repeated
                # (frequency), however we have to add each feature to the log probability unless it has repeated
                # values. Furthermore, the testBOW.txt does not take account punctuation and unseen words in
                # vocabulary.
                probability = (parameters_probability[c][keyword] * items[keyword]) + probability
            sum_log_probabilities[c] = probability + prior_probability[c]
            probability = 0
    return y_arg_max(sum_log_probabilities)


def init_naive_bayes_classifier(directory):
    training_file = directory + "/trainBOW.txt"
    bow = {}
    total_documents, total_doc_per_class, classes = total_number_documents()
    bow = upload_train_data(training_file, classes)
    # Training a Naive Bayes Classifier
    prior_probability, parameters_probability, vocabulary = NB_classifier(bow, classes, total_doc_per_class,
                                                                          total_documents)
    if directory == "movie-review-small":
        name = "movie-review-small-BOW.NB"
    else:
        name = "movie-review-BOW.NB"
    print ("Creating parameters of BOW: " + name + '\n')
    create_file_parameters(name, prior_probability, parameters_probability)

    # Testing a document in Naive Bayes Classifier
    # Testing a file that it has been pre-processed to get a text without punctuation and unseen words in vocabulary.
    testing_file = directory + "/testBOW.txt"

    data = upload_test_data(testing_file)

    actual = []
    production = []
    # Test each document in order to get a prediction for them.
    for doc_item in data:  # for each document in testing_file
        actual.append(list(doc_item.keys())[0])
        # It is not necessary to send the vocabulary due the test_training has already been pre-processed.
        production_label = NB_test(doc_item, prior_probability, parameters_probability, classes)
        production.append(production_label)

    output_file = "outuput.txt"
    print("Creating output or prediction file: " + output_file + '\n')
    create_file_prediction(output_file, actual, production)


print("Insert the directory name to start with naive bayes classifier: ")
directory = input()
path = directory + "/train"
init_naive_bayes_classifier(directory)