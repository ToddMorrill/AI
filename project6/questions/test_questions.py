import math
import time

import pytest

from questions import load_files, tokenize, compute_idfs, top_files, top_sentences


def test_load_files():
    with open('corpus/natural_language_processing.txt', 'r') as f:
        expected = f.read()
    content_dict = load_files('corpus')
    assert content_dict['natural_language_processing.txt'] == expected


def test_tokenize():
    original = 'The quick brown fox jumped over the lazy dog.'
    expected = ['quick', 'brown', 'fox', 'jumped', 'lazy', 'dog']
    result = tokenize(original)
    assert result == expected


@pytest.fixture()
def documents():
    files = load_files('corpus')
    file_words = {filename: tokenize(files[filename]) for filename in files}
    return file_words


def test_compute_idfs(documents):
    idf_dict = compute_idfs(documents)
    # 'learned' appears in 'neural_network.txt', 'machine_learning.txt'
    expected = math.log(len(documents) / 2)
    assert idf_dict['learned'] == expected


def test_top_files():
    doc_1 = 'Artificial Intelligence is changing the world.'
    doc_2 = 'Intelligence is the hallmark of Homo Sapiens.'
    doc_3 = 'Artificial food additives are best avoided.'
    files = {'doc_1': doc_1, 'doc_2': doc_2, 'doc_3': doc_3}
    file_words = {filename: tokenize(files[filename]) for filename in files}
    query = set(tokenize('artificial intelligence rocks!'))
    idfs = compute_idfs(file_words)
    n = 2
    # add a fourth doc, excluded from original idf computation
    doc_4 = tokenize(
        'Artificial intelligence marks the fourth industrial revolution.')
    file_words['doc_4'] = doc_4
    expected = ['doc_1', 'doc_4']
    result = top_files(query, file_words, idfs, n)
    assert expected == result

def test_top_sentences():
    sent_1 = 'Artificial Intelligence is changing the world.'
    sent_2 = 'Intelligence is the hallmark of Homo Sapiens.'
    sent_3 = 'Artificial food additives are best avoided.'
    sentences = {sent_1: sent_1, sent_2: sent_2, sent_3: sent_3}
    sent_words = {filename: tokenize(sentences[filename]) for filename in sentences}
    query = set(tokenize('artificial intelligence rocks!'))
    idfs = compute_idfs(sent_words)
    n = 2
    # add a fourth doc, excluded from original idf computation
    sent_4 = 'Artificial intelligence marks the fourth industrial revolution.'
    sent_words[sent_4] = tokenize(sent_4)
    expected = [sent_1, sent_4]
    result = top_sentences(query, sent_words, idfs, n)
    assert expected == result
