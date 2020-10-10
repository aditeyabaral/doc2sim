import sys
import utils

filenames = sys.argv[1:]

if filenames:
    similarity_matrix = utils.check_similarity(filenames)
    print(f"\nSimilarity = \n{similarity_matrix}")
else:
    print('\nUsage: doc2sim.py file1 file2 file3\n')
