# The City University of New York, Queens College
# Instructor: Alla Rozovskaya
# Student: Edgar Lizarraga-Ugarte
# CSCI780: Natural Language Processing / Fall 2019

The following lines are the instructions to run the application:

1.- Create a directory. For example "bayesClassifier"
2.- Put the following folders or files in the same directory that was created in step 1:
    movie-review-small/ - folder
    NB.py               - file
    pre-process.py      - file
    aclImdb/            - folder
    *movie-review/test       - to dowload from professor's google drive
    *movie-review/train      - to dowload from professor's google drive


3-. Run the following command in your terminal:
    python pre-process.py
4-. Insert the directory name to pre-process:
    Example: movie-review-small
    If you would like to pre-process the huge movie review classification, you should download the movie-review/test and movie-review/train folders.

5.- Indicate what do you want to train (train/test partition):
    Example: train

6.- To test a test partition, we should go to step 3 and put "test" in step 5

7.- In order to run NB_classifier, you should run the following command in your terminal:
    python NB.py

8.- Insert the directory name to start with naive bayes classifier:
    Example: movie-review-small
    It could be movie-review, but it has to be downloaded from google drive repository

Results are in:
movie-review-small-BOW.NB
outuput.txt
trainBOW.txt
testBOW.txt

Note: The project was interpreted by a python 3.7 version