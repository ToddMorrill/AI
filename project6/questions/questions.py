"""This module implements a question-answering system to retrieve relevant
 passages from a corpus of documents given a query string.

Examples:
    $ python3 questions.py corpus
"""

from collections import defaultdict, Counter
import math
import os
import string
import sys

import nltk

FILE_MATCHES = 3
SENTENCE_MATCHES = 3


def load_files(directory: str) -> dict:
    """Given a directory name, return a dictionary mapping the filename of each
     `.txt` file inside that directory to the file's contents as a string.

    Args:
        directory (str): Directory containing document files.

    Returns:
        dict: Dictionary mapping filenames to string content.
    """
    file_dict = {}
    filenames = os.listdir(directory)
    for file in filenames:
        file_path = os.path.join(directory, file)
        with open(file_path, 'r') as f:
            contents = f.read()
        file_dict[file] = contents
    return file_dict


def tokenize(document: string) -> list:
    """Given a document (represented as a string), return a list of all of the
     words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
     punctuation or English stopwords.

    Args:
        document (string): String of text to be processed.

    Returns:
        list: List of processed words from the document.
    """
    document = document.lower()
    tokens = nltk.word_tokenize(document)

    # filter out punctuation and stopwords
    cleaned_tokens = []
    for token in tokens:
        # break into 2 if statements to reduce compute time
        if token in string.punctuation:
            continue
        if token in nltk.corpus.stopwords.words('english'):
            continue
        cleaned_tokens.append(token)
    return cleaned_tokens


def compute_idfs(documents: dict) -> dict:
    """Given a dictionary of `documents` that maps names of documents to a list
     of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
     resulting dictionary.

    Args:
        documents (dict): A mapping of file names to words in the document.

    Returns:
        dict: A mapping of words to their IDF values.
    """
    num_docs = len(documents)

    words_to_docs = defaultdict(set)
    for doc in documents:
        for word in documents[doc]:
            words_to_docs[word].add(doc)

    idf_scores = {}
    for word in words_to_docs:
        num_docs_word_appears = len(words_to_docs[word])
        idf_scores[word] = math.log(num_docs / num_docs_word_appears)

    return idf_scores


def top_files(query: set, files: dict, idfs: dict, n: int) -> list:
    """Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the `n` top
    files that match the query, ranked according to tf-idf.

    Args:
        query (set): A set of query words.
        files (dict): A mapping of file names to words in the document.
        idfs (dict): A mapping of words to their IDF values.
        n (int): The number of file names to return.

    Returns:
        list: The ranked list of n file names.
    """
    # compute term frequencies for each doc's words
    tfs = {}
    for file in files:
        tfs[file] = Counter(files[file])

    # compute sum of tf-idf words score for each query word in each doc
    file_tf_idf_scores = []
    for file in files:
        running_sum = 0
        for word in query:
            # need to check if word is present in both dictionaries
            if (word in tfs[file]) and (word in idfs):
                running_sum += tfs[file][word] * idfs[word]
        file_tf_idf_scores.append((file, running_sum))

    # sort files by tf-idf score
    file_tf_idf_scores.sort(key=lambda x: x[1], reverse=True)
    file_names, scores = zip(*file_tf_idf_scores)
    return list(file_names[:n])


def top_sentences(query: set, sentences: dict, idfs: dict, n: int) -> list:
    """Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.

    Args:
        query (set): A set of query words.
        sentences (dict): A mapping from sentence strings to the words
             contained in the sentence.
        idfs (dict): A mapping of words to their IDF values.
        n (int): The number of file names to return.

    Returns:
        list: The ranked list of n sentences.
    """
    # compute term frequencies for each sentence's words, useful for:
    # 1) indexing words for faster lookups and 2) computing query term density
    tfs = {}
    for sentence in sentences:
        tfs[sentence] = Counter(sentences[sentence])

    file_idf_qtd_scores = []
    for sentence in sentences:
        # compute IDF and QTD scores for each sentence
        idf_running_sum = 0
        qtd_numerator = 0
        for word in query:
            if (word in tfs[sentence]) and (word in idfs):
                idf_running_sum += idfs[word]

            # QTD score numerator
            if (word in tfs[sentence]):
                qtd_numerator += tfs[sentence][word]

        qtd_score = qtd_numerator / len(sentences[sentence])

        # maintain in a list
        file_idf_qtd_scores.append((sentence, idf_running_sum, qtd_score))

    # sort on IDF scores, then QTD scores
    file_idf_qtd_scores.sort(key=lambda x: (x[1], x[2]), reverse=True)

    file_names, idf_scores, qtd_scores = zip(*file_idf_qtd_scores)
    return list(file_names[:n])


def main():
    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {filename: tokenize(files[filename]) for filename in files}
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


if __name__ == "__main__":
    main()
