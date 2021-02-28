from collections import Counter, defaultdict
import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def crawl(directory: str) -> dict:
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(link for link in pages[filename]
                              if link in pages)

    return pages


def transition_model(corpus: dict, page: str, damping_factor: float) -> dict:
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    uniform_prob = 1 / len(corpus)

    # if empty set, uniform dist. over all pages
    if not corpus[page]:
        transition_probs = {key: uniform_prob for key in corpus}
        return transition_probs

    # every node is assigned uniform * (1 - damping_factor) prob
    dampened_uniform_prob = uniform_prob * (1 - damping_factor)
    transition_probs = {key: dampened_uniform_prob for key in corpus}

    # neighbors are given additional damping_factor / len(neighbors) prob
    out_degree = len(corpus[page])
    additional_weight = damping_factor / out_degree
    for neighbor in corpus[page]:
        transition_probs[neighbor] += additional_weight

    return transition_probs


def _sample_states(corpus: dict, damping_factor: float, n: int) -> Counter:
    # keep track of state counts
    counter = Counter()

    # choose random starting page
    page = random.choice(list(corpus.keys()))
    counter[page] += 1
    transition_probs = transition_model(corpus, page, damping_factor)

    # sample the remaining n-1 states
    for _ in range(n - 1):
        page = random.choices(list(transition_probs.keys()),
                              list(transition_probs.values()),
                              k=1)[0]
        counter[page] += 1
        transition_probs = transition_model(corpus, page, damping_factor)

    return counter


def sample_pagerank(corpus: dict, damping_factor: float, n: int) -> dict:
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # sample n states
    state_counts = _sample_states(corpus, damping_factor, n)

    # warn if not all states were sampled
    missing_keys = set(corpus.keys()) - set(state_counts.keys())
    if missing_keys:
        print(
            'WARNING: Not all corpus states were sampled. Consider increasing '
            'the number of sampled states \'n\'.')
        for key in missing_keys:
            state_counts[key] = 0.0

    # normalize counts and sort in descending order
    pagerank_dist = {
        key: val / n
        for key, val in sorted(state_counts.items(), key=lambda x: x[1])
    }
    return pagerank_dist


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    uniform_prob = 1 / len(corpus)
    pagerank_dist = {key: uniform_prob for key in corpus}
    random_hop = (1 - damping_factor) / len(corpus)
    inverted_corpus = defaultdict(set)
    for key in corpus:
        # if no neighbors, add all pages as neighbors
        if not corpus[key]:
            for neighbor in corpus:
                inverted_corpus[neighbor].add(key)
        # otherwise, just add neighbors
        else:
            for neighbor in corpus[key]:
                inverted_corpus[neighbor].add(key)

    # these should really be a global vars or passed arguments
    MAX_ITER = 1000
    TOLERANCE = 1e-3

    # only iterate for a max of specified number of steps
    for _ in range(MAX_ITER):
        # monitor changes to the distribution between iterations
        pagerank_new_dist = dict()

        # update scores for each page
        for page in pagerank_dist:
            # if no inbound neighbors

            # initialize with random hop
            pagerank_new_dist[page] = random_hop

            # get inbound neighbors and update score for each neighbor
            neighbors_sum = 0
            for neighbor in inverted_corpus[page]:
                # out degree is number if pages if no out links
                out_degree = len(
                    corpus[neighbor]) if corpus[neighbor] else len(corpus)
                # neighbor score / out_degree of neighbor
                neighbors_sum += pagerank_dist[neighbor] / out_degree
            pagerank_new_dist[page] += damping_factor * neighbors_sum

        # check if changes are below the tolerance
        close = []
        for key in pagerank_dist:
            diff = abs(pagerank_dist[key] - pagerank_new_dist[key])
            close.append(diff < TOLERANCE)

        if all(close):
            return pagerank_new_dist
        # o/w continue iterating
        pagerank_dist = pagerank_new_dist
    # raise error that model didn't converge
    raise Exception('Iterative PageRank failed to converge.')


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


if __name__ == "__main__":
    main()
