
import re
import math
from collections import Counter


def tokenize(text):
    return re.findall(r'\b[a-z0-9+#.]+\b', text.lower())


def calculate_text_similarity(resume_text, job_description):

    resume_words = tokenize(resume_text)
    job_words = tokenize(job_description)

    if not resume_words or not job_words:
        return 0

    documents = [resume_words, job_words]

    word_counts = [Counter(doc) for doc in documents]

    vocabulary = set(resume_words + job_words)

    vectors = []

    total_documents = len(documents)

    for document_words, counts in zip(documents, word_counts):

        total_words = len(document_words)
        vector = {}

        for word in vocabulary:

            document_frequency = sum(
                1 for doc in documents if word in doc
            )

            tf = counts[word] / total_words

            idf = math.log(
                (1 + total_documents) /
                (1 + document_frequency)
            ) + 1

            vector[word] = tf * idf

        vectors.append(vector)

    vector_a, vector_b = vectors

    dot_product = sum(
        vector_a[word] * vector_b[word]
        for word in vocabulary
    )

    magnitude_a = math.sqrt(
        sum(value ** 2 for value in vector_a.values())
    )

    magnitude_b = math.sqrt(
        sum(value ** 2 for value in vector_b.values())
    )

    if magnitude_a == 0 or magnitude_b == 0:
        return 0

    similarity = dot_product / (magnitude_a * magnitude_b)

    return round(similarity * 100, 2)
