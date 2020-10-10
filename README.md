# doc2sim
A simple command line utility to find similarity in content between documents using Doc2Vec.

Although the metric isn't completely accurate, it is capable of providing a good metric to perform a plagiarism check. It uses cosine similarity to find the similarity between documents and returns a similarity matrix. The tool works for an arbitrary number of text containing documents like .docx, .pdf, .txt, .c and so on.

# How to run doc2sim
To use doc2sim on command line, use
```bash
python3 doc2sim.py file1 file2
```
Alternatively, run the flask app with

```bash
./server-dev.run
```
