import pytest
import networkx

from pagerank import crawl, sample_pagerank, iterate_pagerank
from pagerank import DAMPING, SAMPLES, TOLERANCE, MAX_ITER

@pytest.fixture(scope='module')
def expected(corpus):
    g = networkx.DiGraph()
    g.add_nodes_from(corpus)
    # g.add_edges_from()
    expected = networkx.pagerank(g)
    return expected

def test_sample_pagerank(corpus, expected):
    corpus = crawl(corpus)
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    assert ranks == expected
    

def test_iterate_pagerank(corpus):
    corpus = crawl(corpus)
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
