from nltk import Tree
import pytest

from parser import preprocess, parser, np_chunk


@pytest.mark.parametrize(
    'sentence,expected',
    [('Holmes sat.', ['holmes', 'sat']),
     ('This is as easy as 123.', ['this', 'is', 'as', 'easy', 'as']),
     ('Alpha123 123 !! ALPHA!', ['alpha123', 'alpha'])])
def test_preprocess_one(sentence, expected):
    words = preprocess(sentence)
    assert words == expected


def test_valid_1():
    s = 'Holmes sat in the armchair.'
    words = preprocess(s)
    trees = parser.parse(words)
    result = next(trees)
    expected = Tree('S', [Tree('NP', [Tree('Nbar', [Tree('N', ['holmes'])])]), Tree('VP', [Tree('V', ['sat']), Tree('PP', [Tree('P', ['in']), Tree('NP', [Tree('Det', ['the']), Tree('Nbar', [Tree('N', ['armchair'])])])])])])
    assert result == expected


def test_valid_2():
    s = 'Holmes sat in the red armchair.'
    words = preprocess(s)
    trees = parser.parse(words)
    result = next(trees)
    expected = Tree('S', [Tree('NP', [Tree('Nbar', [Tree('N', ['holmes'])])]), Tree('VP', [Tree('V', ['sat']), Tree('PP', [Tree('P', ['in']), Tree('NP', [Tree('Det', ['the']), Tree('Nbar', [Tree('AP', [Tree('Adj', ['red'])]), Tree('Nbar', [Tree('N', ['armchair'])])])])])])])
    assert result == expected

def test_valid_3():
    s = 'Holmes sat in the little red armchair.'
    words = preprocess(s)
    trees = parser.parse(words)
    result = next(trees)
    expected = Tree('S', [Tree('NP', [Tree('Nbar', [Tree('N', ['holmes'])])]), Tree('VP', [Tree('V', ['sat']), Tree('PP', [Tree('P', ['in']), Tree('NP', [Tree('Det', ['the']), Tree('Nbar', [Tree('AP', [Tree('Adj', ['little']), Tree('AP', [Tree('Adj', ['red'])])]), Tree('Nbar', [Tree('N', ['armchair'])])])])])])])
    assert result == expected

def test_parser_invalid_1():
    # test invalid sentence
    s = 'The the red door sat.'
    words = preprocess(s)
    trees = parser.parse(words)
    try:
        # shouldn't be able to parse
        next(trees)
    except StopIteration:
        assert True

def test_parser_invalid_2():
    # test invalid sentence
    s = 'Armchair on the sat Holmes.'
    words = preprocess(s)
    trees = parser.parse(words)
    try:
        # shouldn't be able to parse
        next(trees)
    except StopIteration:
        assert True

def test_parser_invalid_3():
    # test invalid sentence
    s = 'Holmes sat in the the armchair.'
    words = preprocess(s)
    trees = parser.parse(words)
    try:
        # shouldn't be able to parse
        next(trees)
    except StopIteration:
        assert True

def test_parser_1():
    with open('sentences/1.txt') as f:
        s = f.read()
    words = preprocess(s)
    trees = parser.parse(words)
    result = next(trees)
    expected = Tree('S', [Tree('NP', [Tree('Nbar', [Tree('N', ['holmes'])])]), Tree('VP', [Tree('V', ['sat'])])])
    assert result == expected


def test_parser_2():
    with open('sentences/2.txt') as f:
        s = f.read()
    words = preprocess(s)
    trees = parser.parse(words)
    result = next(trees)
    expected = Tree('S', [Tree('NP', [Tree('Nbar', [Tree('N', ['holmes'])])]), Tree('VP', [Tree('V', ['lit']), Tree('NP', [Tree('Det', ['a']), Tree('Nbar', [Tree('N', ['pipe'])])])])])
    assert result == expected


def test_parser_3():
    with open('sentences/3.txt') as f:
        s = f.read()
    words = preprocess(s)
    trees = parser.parse(words)
    result = next(trees)
    # breakpoint()
    # result.pretty_print()
    expected = Tree('S', [Tree('NP', [Tree('Nbar', [Tree('N', ['we'])])]), Tree('VP', [Tree('V', ['arrived']), Tree('NP', [Tree('Det', ['the']), Tree('Nbar', [Tree('Nbar', [Tree('N', ['day'])]), Tree('PP', [Tree('P', ['before']), Tree('NP', [Tree('Nbar', [Tree('N', ['thursday'])])])])])])])])
    assert result == expected


def test_parser_4():
    with open('sentences/4.txt') as f:
        s = f.read()
    words = preprocess(s)
    trees = parser.parse(words)
    result = next(trees)
    expected = Tree('S', [Tree('S', [Tree('NP', [Tree('Nbar', [Tree('N', ['holmes'])])]), Tree('VP', [Tree('V', ['sat']), Tree('PP', [Tree('P', ['in']), Tree('NP', [Tree('Det', ['the']), Tree('Nbar', [Tree('AP', [Tree('Adj', ['red'])]), Tree('Nbar', [Tree('N', ['armchair'])])])])])])]), Tree('Conj', ['and']), Tree('S', [Tree('NP', [Tree('Nbar', [Tree('N', ['he'])])]), Tree('VP', [Tree('V', ['chuckled'])])])])
    assert result == expected


def test_parser_5():
    with open('sentences/5.txt') as f:
        s = f.read()
    words = preprocess(s)
    trees = parser.parse(words)
    result = next(trees)
    expected = Tree('S', [Tree('NP', [Tree('Det', ['my']), Tree('Nbar', [Tree('N', ['companion'])])]), Tree('VP', [Tree('V', ['smiled']), Tree('NP', [Tree('Det', ['an']), Tree('Nbar', [Tree('AP', [Tree('Adj', ['enigmatical'])]), Tree('Nbar', [Tree('N', ['smile'])])])])])])
    assert result == expected


def test_parser_6():
    with open('sentences/6.txt') as f:
        s = f.read()
    words = preprocess(s)
    trees = parser.parse(words)
    result = next(trees)
    expected = Tree('S', [Tree('NP', [Tree('Nbar', [Tree('N', ['holmes'])])]), Tree('VP', [Tree('V', ['chuckled']), Tree('PP', [Tree('P', ['to']), Tree('NP', [Tree('Nbar', [Tree('N', ['himself'])])])])])])
    assert result == expected


def test_parser_7():
    with open('sentences/7.txt') as f:
        s = f.read()
    words = preprocess(s)
    trees = parser.parse(words)
    result = next(trees)
    expected = Tree('S', [Tree('S', [Tree('NP', [Tree('Nbar', [Tree('N', ['she'])])]), Tree('VP', [Tree('AdvP', [Tree('Adv', ['never'])]), Tree('VP', [Tree('V', ['said']), Tree('NP', [Tree('Det', ['a']), Tree('Nbar', [Tree('N', ['word'])])])])])]), Tree('Conj', ['until']), Tree('S', [Tree('NP', [Tree('Nbar', [Tree('N', ['we'])])]), Tree('VP', [Tree('VP', [Tree('V', ['were']), Tree('PP', [Tree('P', ['at']), Tree('NP', [Tree('Det', ['the']), Tree('Nbar', [Tree('N', ['door'])])])])]), Tree('AdvP', [Tree('Adv', ['here'])])])])])
    assert result == expected


def test_parser_8():
    # hacky solution, need to revisit
    with open('sentences/8.txt') as f:
        s = f.read()
    words = preprocess(s)
    trees = parser.parse(words)
    result = next(trees)
    expected = Tree('S', [Tree('NP', [Tree('Nbar', [Tree('N', ['holmes'])])]), Tree('VP', [Tree('VP', [Tree('VP', [Tree('V', ['sat'])]), Tree('AdvP', [Tree('Adv', ['down'])])]), Tree('Conj', ['and']), Tree('VP', [Tree('V', ['lit']), Tree('NP', [Tree('Det', ['his']), Tree('Nbar', [Tree('N', ['pipe'])])])])])])
    assert result == expected


def test_parser_9():
    # hacky solution, need to revisit
    with open('sentences/9.txt') as f:
        s = f.read()
    words = preprocess(s)
    trees = parser.parse(words)
    result = next(trees)
    expected = Tree('S', [Tree('NP', [Tree('Nbar', [Tree('N', ['i'])])]), Tree('VP', [Tree('VP', [Tree('V', ['had']), Tree('NP', [Tree('Det', ['a']), Tree('Nbar', [Tree('Nbar', [Tree('AP', [Tree('Adj', ['country'])]), Tree('Nbar', [Tree('N', ['walk'])])]), Tree('PP', [Tree('P', ['on']), Tree('NP', [Tree('Nbar', [Tree('N', ['thursday'])])])])])])]), Tree('Conj', ['and']), Tree('VP', [Tree('V', ['came']), Tree('NP', [Tree('Nbar', [Tree('Nbar', [Tree('N', ['home'])]), Tree('PP', [Tree('P', ['in']), Tree('NP', [Tree('Det', ['a']), Tree('Nbar', [Tree('AP', [Tree('Adj', ['dreadful'])]), Tree('Nbar', [Tree('N', ['mess'])])])])])])])])])])
    assert result == expected


def test_parser_10():
    with open('sentences/10.txt') as f:
        s = f.read()
    words = preprocess(s)
    trees = parser.parse(words)
    result = next(trees)
    # breakpoint()
    # result.pretty_print()
    expected = Tree('S', [Tree('NP', [Tree('Nbar', [Tree('N', ['i'])])]), Tree('VP', [Tree('V', ['had']), Tree('NP', [Tree('Det', ['a']), Tree('Nbar', [Tree('AP', [Tree('Adj', ['little']), Tree('AP', [Tree('Adj', ['moist']), Tree('AP', [Tree('Adj', ['red'])])])]), Tree('Nbar', [Tree('Nbar', [Tree('Nbar', [Tree('N', ['paint'])]), Tree('PP', [Tree('P', ['in']), Tree('NP', [Tree('Det', ['the']), Tree('Nbar', [Tree('N', ['palm'])])])])]), Tree('PP', [Tree('P', ['of']), Tree('NP', [Tree('Det', ['my']), Tree('Nbar', [Tree('N', ['hand'])])])])])])])])])
    assert result == expected

def test_np_chunk_1():
    # simple test with one NP
    tree = Tree('S', [Tree('NP', ['simple'])])
    expected = [Tree('NP', ['simple'])]
    result = np_chunk(tree)
    assert result == expected

def test_np_chunk_2():
    # nested NP
    tree = Tree('NP', [Tree('NP', ['simple'])])
    expected = [Tree('NP', ['simple'])]
    result = np_chunk(tree)
    assert result == expected

def test_np_chunk_3():
    # doubly nested NP
    tree = Tree('NP', [Tree('NP', ['simple', Tree('NP', ['sentence'])])])
    expected = [Tree('NP', ['sentence'])]
    result = np_chunk(tree)
    assert result == expected

def test_np_chunk_4():
    # two NPs side-by-side
    tree = Tree('S', [Tree('NP', [Tree('Adj', ['simple']), Tree('N', ['sentence'])]), Tree('NP', [Tree('Conj', ['and']), Tree('N', ['another'])])])
    expected = [Tree('NP', [Tree('Adj', ['simple']), Tree('N', ['sentence'])]), Tree('NP', [Tree('Conj', ['and']), Tree('N', ['another'])])]
    result = np_chunk(tree)
    assert result == expected