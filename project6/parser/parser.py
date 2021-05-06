"""This module implements a noun-phrase parser.

Examples:
    $ python3 parser.py sentences/1.txt

Timing:
30 + 20 + 20
"""
import nltk
import re
import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

# consider using VP PP to account for multiple prepositional phrases (e.g. from x to y)
NONTERMINALS = """
S -> NP VP | S Conj S
VP -> V | V NP | V PP | AdvP VP | VP AdvP | VP Conj VP
PP -> P NP
NP -> Nbar | Det Nbar | Nbar Conj Nbar
AP -> Adj | Adj AP
AdvP -> Adv | Adv AdvP
Nbar -> N | AP Nbar | Nbar PP
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    sentence = sentence.lower()
    words = nltk.word_tokenize(sentence)
    words = [x for x in words if re.search('[a-zA-Z]', x)]
    return words


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    np_chunks = []
    # retrieve all NP subtrees
    for sub in tree.subtrees(filter=lambda t: t.label() == 'NP'):
        # check if subtree contains any NP subtrees other than itself
        np_subtrees = list(sub.subtrees(filter=lambda t: t.label() == 'NP'))
        if len(np_subtrees) == 1:
            np_chunks.append(sub)
    return np_chunks


def main():
    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


if __name__ == "__main__":
    main()
