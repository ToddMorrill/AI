# run solver 100 times to determine if interleaving ac3 is speeding things up
import time

from generate import CrosswordCreator
from crossword import Crossword


def large_crossword():
    structure = 'data/structure2.txt'
    words = 'data/words2.txt'
    crossword = Crossword(structure, words)
    return crossword


def run_solve():
    times = []
    for i in range(100):
        creator = CrosswordCreator(large_crossword())
        start = time.time()
        creator.solve()
        end = time.time()
        duration = end-start
        times.append(duration)
    
    # average run times
    print(sum(times) / len(times))

run_solve()