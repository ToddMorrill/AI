import math
import time

import pytest

from questions import load_files, tokenize, compute_idfs


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