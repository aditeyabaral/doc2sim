import sys
import numpy as np
from nltk.tokenize import word_tokenize, sent_tokenize
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from readDocument import getText


def cosine_similarity(A, B):
    return np.dot(A, B)/(np.linalg.norm(A)*np.linalg.norm(B))


filenames = sys.argv[1:]
documents = list(map(getText, filenames))
train_text = [TaggedDocument(words=word_tokenize(
    doc), tags=[str(i)]) for i, doc in enumerate(documents)]


print("Creating Doc2Vec model...")
model = Doc2Vec(vector_size=500, window=2, epochs=20, min_count=1)
model.build_vocab(train_text)
model.train(train_text, total_examples=model.corpus_count, epochs=50)
print("Training completed...")

print("Obtaining sentences for documents...")
test_text = list(map(word_tokenize, documents))

print("Obtaing Document Vectors...")
vecs = list(map(model.infer_vector, test_text))

print(f"\nSimilarity = {cosine_similarity(*vecs)}")
