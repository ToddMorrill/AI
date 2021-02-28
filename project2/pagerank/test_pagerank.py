import math
from re import S
from networkx.algorithms.link_analysis.pagerank_alg import pagerank

import pytest
import networkx

from pagerank import _sample_states, crawl, transition_model, sample_pagerank, iterate_pagerank
from pagerank import DAMPING, SAMPLES


@pytest.fixture(scope='module', params=['corpus0', 'corpus1', 'corpus2'])
def corpus(request):
    return crawl(request.param)


@pytest.fixture(scope='module')
def toy_corpus():
    return {
        '1.html': {'2.html', '3.html'},
        '2.html': {'3.html'},
        '3.html': {'2.html'}
    }


def test_transition_no_neighbors():
    # NB: recursion doesn't have any outbound links
    sample_corpus = crawl('corpus2')
    probs = transition_model(sample_corpus, 'recursion.html', DAMPING)
    # assert all keys the same
    assert set(sample_corpus.keys()) == set(probs.keys())
    # assert uniform distribution
    uniform_prob = 1 / len(sample_corpus)
    assert all(val == uniform_prob for val in probs.values())


def test_transition_simple(toy_corpus):
    page = '1.html'
    # assuming damping factor 0.85
    expected = {'1.html': 0.05, '2.html': 0.475, '3.html': 0.475}
    result = transition_model(toy_corpus, page, damping_factor=0.85)
    assert result == expected


@pytest.mark.parametrize('damping_factor', [0.75, 0.85])
def test_transition_sum(damping_factor, toy_corpus):
    # arbitrarily choose the first key from the corpus for testing
    page = list(toy_corpus.keys())[0]
    result = transition_model(toy_corpus, page, damping_factor)
    sums_to_one = math.isclose(sum(result.values()), 1.0, abs_tol=1e-6)
    assert sums_to_one


def test_sample_states(toy_corpus):
    state_counts = _sample_states(toy_corpus, DAMPING, SAMPLES)
    # ensure the correct number of samples made it into the counter dict
    assert sum(state_counts.values()) == SAMPLES


def test_sample_pagerank_sum(corpus):
    sample_dist = sample_pagerank(corpus, DAMPING, SAMPLES)
    # ensure the distribution sums to 1
    sums_to_one = math.isclose(sum(sample_dist.values()), 1.0, abs_tol=1e-6)
    assert sums_to_one


def test_sample_pagerank_keys(toy_corpus):
    sample_dist = sample_pagerank(toy_corpus, DAMPING, 2)
    # ensure all keys are present
    assert set(sample_dist.keys()) == set(toy_corpus.keys())


@pytest.fixture(scope='module')
def expected_dist(corpus):
    g = networkx.DiGraph(corpus)
    true_dist = networkx.pagerank(g, alpha=DAMPING, tol=1e-6)
    return corpus, true_dist


def test_sample_pagerank(expected_dist):
    corpus, true_dist = expected_dist
    # need A LOT of samples to converge, and still getting some chatter
    dist = sample_pagerank(corpus, DAMPING, 15000)
    close = []
    for key in dist:
        close.append(math.isclose(dist[key], true_dist[key], abs_tol=1e-1))
    assert all(close)


def test_iterate_pagerank(expected_dist):
    corpus, true_dist = expected_dist
    dist = iterate_pagerank(corpus, DAMPING)
    close = []
    for key in dist:
        close.append(math.isclose(dist[key], true_dist[key], abs_tol=1e-2))
    assert all(close)


def test_implementations_close(corpus):
    # test with default problem specs
    sample_dist = sample_pagerank(corpus, DAMPING, SAMPLES)
    iter_dist = iterate_pagerank(corpus, DAMPING)
    close = []
    for key in sample_dist:
        close.append(
            math.isclose(sample_dist[key], iter_dist[key], abs_tol=1e-1))
    assert all(close)