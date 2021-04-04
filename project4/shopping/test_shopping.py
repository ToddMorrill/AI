import pytest

from shopping import load_data

@pytest.fixture()
def data():
    return load_data('shopping.csv')

def test_first_row(data):
    expected_evidence = [0, 0.0, 0, 0.0, 1, 0.0, 0.2, 0.2, 0.0, 0.0, 1, 1, 1, 1, 1, 1, 0]
    expected_label = 0
    evidence, labels = data
    assert evidence[0] == expected_evidence
    assert labels[0] == expected_label

def test_data_len(data):
    evidence, labels = data
    assert len(evidence) == 12330
    assert len(labels) == 12330
    assert len(evidence[0]) == 17