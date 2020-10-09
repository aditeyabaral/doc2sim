import sys

from pathlib import Path

import doc2sim

filenames = sys.argv[1:]

if filenames:
    similarity_matrix = doc2sim.check_similarity(filenames)
    print(f"\nSimilarity = \n{similarity_matrix}")
else:
    print('\nUsage: d2v.py file1 file2 file3 ...\n')
