"""
Compare BM25 and TF-IDF Retrieval Methods

This script demonstrates and compares two popular lexical retrieval algorithms:
1. BM25 (Best Matching 25)
2. TF-IDF (Term Frequency-Inverse Document Frequency)

These methods are used to retrieve documents based on keyword matching.
The examples illustrate their behavior with different query types and document collections.
"""

import math
import re
from collections import Counter

import matplotlib.pyplot as plt
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Sample document collection for our experiments
documents = [
    "The quick brown fox jumps over the lazy dog",
    "A fox is a cunning animal that adapts well to many environments",
    "Dogs are loyal companions and have been domesticated for thousands of years",
    "Quick reflexes are essential for predators like foxes when hunting",
    "The relationship between humans and dogs has evolved over millennia",
    "Brown bears and red foxes are common in certain forest ecosystems",
    "Lazy afternoons are perfect for dogs to nap in the sunshine",
    "Foxes belong to the Canidae family which also includes wolves and dogs",
]


# Clean and tokenize text (basic preprocessing)
def preprocess(text: str) -> list[str]:
    """Convert text to lowercase, remove punctuation and split into words."""
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)  # Remove punctuation
    return text.split()


# ==================== TF-IDF IMPLEMENTATION ====================


def calculate_tf_idf_sklearn(documents: list[str], query: str):
    """
    Use scikit-learn's implementation to calculate TF-IDF scores.

    Args:
        documents: List of document strings
        query: Query string

    Returns:
        Sorted list of (document_index, similarity_score) tuples
    """
    # Initialize TF-IDF vectorizer
    vectorizer = TfidfVectorizer()

    # Create document-term matrix
    tfidf_matrix = vectorizer.fit_transform(documents)

    # Transform query to the same vector space
    query_vector = vectorizer.transform([query])

    # Calculate cosine similarity between query and all documents
    similarities = cosine_similarity(query_vector, tfidf_matrix).flatten()

    # Sort documents by similarity score (descending)
    ranked_results = [(i, score) for i, score in enumerate(similarities)]
    ranked_results.sort(key=lambda x: x[1], reverse=True)

    return ranked_results


def calculate_tf_idf_manual(documents: list[str], query: str):
    """
    Manual implementation of TF-IDF to demonstrate the mechanics.

    Args:
        documents: List of document strings
        query: Query string

    Returns:
        Sorted list of (document_index, similarity_score) tuples
    """
    # Preprocess all documents and the query
    processed_docs = [preprocess(doc) for doc in documents]
    processed_query = preprocess(query)

    # Create vocabulary from all documents
    all_terms = set()
    for doc in processed_docs:
        all_terms.update(doc)

    # Calculate document frequencies
    doc_freq = {}
    for term in all_terms:
        doc_freq[term] = sum(1 for doc in processed_docs if term in doc)

    # Calculate IDF for each term
    num_docs = len(documents)
    idf = {term: math.log(num_docs / (df)) for term, df in doc_freq.items()}

    # Calculate TF-IDF for each document
    tfidf_vectors = []
    for doc in processed_docs:
        # Count term frequencies
        term_freq = Counter(doc)

        # Calculate TF-IDF vector
        doc_vector = {term: tf * idf.get(term, 0) for term, tf in term_freq.items()}
        tfidf_vectors.append(doc_vector)

    # Calculate TF-IDF for query
    query_tf = Counter(processed_query)
    query_vector = {term: tf * idf.get(term, 0) for term, tf in query_tf.items()}

    # Calculate cosine similarity between query and each document
    similarities = []
    for i, doc_vector in enumerate(tfidf_vectors):
        # Find common terms
        common_terms = set(query_vector.keys()) & set(doc_vector.keys())

        # Calculate dot product
        dot_product = sum(query_vector[term] * doc_vector[term] for term in common_terms)

        # Calculate magnitudes
        query_mag = math.sqrt(sum(val**2 for val in query_vector.values()))
        doc_mag = math.sqrt(sum(val**2 for val in doc_vector.values()))

        # Calculate cosine similarity (handle division by zero)
        if query_mag > 0 and doc_mag > 0:
            similarity = dot_product / (query_mag * doc_mag)
        else:
            similarity = 0

        similarities.append((i, similarity))

    # Sort documents by similarity score (descending)
    similarities.sort(key=lambda x: x[1], reverse=True)
    return similarities


# ==================== BM25 IMPLEMENTATION ====================


def calculate_bm25(documents: list[str], query: str, k1=1.5, b=0.75):
    """
    Implementation of the BM25 algorithm.

    Args:
        documents: List of document strings
        query: Query string
        k1: Term frequency saturation parameter (default 1.5)
        b: Document length normalization parameter (default 0.75)

    Returns:
        Sorted list of (document_index, score) tuples
    """
    # Preprocess all documents and the query
    processed_docs = [preprocess(doc) for doc in documents]
    processed_query = preprocess(query)

    # Calculate document lengths and average length
    doc_lengths = [len(doc) for doc in processed_docs]
    avg_doc_length = sum(doc_lengths) / len(doc_lengths)

    # Calculate document frequencies
    doc_freq = {}
    all_terms = set()
    for doc in processed_docs:
        all_terms.update(doc)

    for term in all_terms:
        doc_freq[term] = sum(1 for doc in processed_docs if term in doc)

    # Calculate term frequencies for each document
    term_freqs = []
    for doc in processed_docs:
        term_freqs.append(Counter(doc))

    # Calculate BM25 score for each document
    num_docs = len(documents)
    scores = []

    for i, _doc in enumerate(processed_docs):
        score = 0
        doc_len = doc_lengths[i]

        for term in processed_query:
            if term in doc_freq:
                # IDF component using BM25 formula
                idf = math.log((num_docs - doc_freq[term] + 0.5) / (doc_freq[term] + 0.5) + 1)

                # TF component with saturation and document length normalization
                tf = term_freqs[i][term]
                tf_component = tf * (k1 + 1) / (tf + k1 * (1 - b + b * doc_len / avg_doc_length))

                score += idf * tf_component

        scores.append((i, score))

    # Sort documents by score (descending)
    scores.sort(key=lambda x: x[1], reverse=True)
    return scores


# ==================== COMPARISON EXPERIMENTS ====================


def run_comparison(query: str, k1_values=(1.2, 2.0), b_values=(0.75, 0.5)):
    """
    Run a comprehensive comparison of TF-IDF and BM25 for a given query.

    Args:
        query: Query string to search with
        k1_values: List of k1 parameter values to test for BM25
        b_values: List of b parameter values to test for BM25
    """
    print(f"\n{'=' * 80}\nQUERY: '{query}'\n{'=' * 80}")

    # Run TF-IDF using scikit-learn
    tfidf_sklearn_results = calculate_tf_idf_sklearn(documents, query)
    print("\nTF-IDF Results (sklearn):")
    for i, (doc_idx, score) in enumerate(tfidf_sklearn_results):
        print(f"{i + 1}. [{score:.4f}] Document {doc_idx}: {documents[doc_idx]}")

    # Run TF-IDF using manual implementation
    tfidf_manual_results = calculate_tf_idf_manual(documents, query)
    print("\nTF-IDF Results (manual implementation):")
    for i, (doc_idx, score) in enumerate(tfidf_manual_results):
        print(f"{i + 1}. [{score:.4f}] Document {doc_idx}: {documents[doc_idx]}")

    # Run BM25 with different parameter settings
    for k1 in k1_values:
        for b in b_values:
            bm25_results = calculate_bm25(documents, query, k1=k1, b=b)
            print(f"\nBM25 Results (k1={k1}, b={b}):")
            for i, (doc_idx, score) in enumerate(bm25_results):
                print(f"{i + 1}. [{score:.4f}] Document {doc_idx}: {documents[doc_idx]}")


# ==================== VISUALIZATION ====================


def visualize_algorithm_differences():
    """
    Create visualizations to show differences between TF-IDF and BM25 algorithms.
    """
    # Example showing TF saturation difference between TF-IDF and BM25
    tf_values = np.arange(1, 21)  # Term frequencies from 1 to 20

    # TF-IDF uses raw term frequency
    tfidf_tf_component = tf_values

    # BM25 with different k1 values
    k1_values = [0.5, 1.2, 2.0, 5.0]
    bm25_tf_components = {}
    for k1 in k1_values:
        bm25_tf_components[k1] = [tf * (k1 + 1) / (tf + k1) for tf in tf_values]

    # Create plot
    plt.figure(figsize=(10, 6))
    plt.plot(tf_values, tfidf_tf_component, label="TF-IDF (raw TF)", linewidth=2)

    for k1, values in bm25_tf_components.items():
        plt.plot(tf_values, values, label=f"BM25 (k1={k1})", linestyle="--")

    plt.xlabel("Term Frequency", fontsize=12)
    plt.ylabel("Score Component", fontsize=12)
    plt.title("Term Frequency Saturation in TF-IDF vs BM25", fontsize=14)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig("tf_saturation_comparison.png")

    # Example showing document length normalization in BM25
    doc_lengths = np.arange(10, 210, 10)  # Document lengths from 10 to 200
    avg_doc_length = 100  # Average document length
    term_freq = 5  # Fixed term frequency
    k1 = 1.5  # Fixed k1

    # BM25 with different b values
    b_values = [0, 0.25, 0.5, 0.75, 1.0]
    bm25_length_components = {}

    for b in b_values:
        bm25_length_components[b] = [
            term_freq * (k1 + 1) / (term_freq + k1 * (1 - b + b * doc_len / avg_doc_length))
            for doc_len in doc_lengths
        ]

    # Create plot
    plt.figure(figsize=(10, 6))

    for b, values in bm25_length_components.items():
        plt.plot(doc_lengths, values, label=f"BM25 (b={b})", linewidth=2)

    plt.axhline(y=term_freq, color="r", linestyle="-", label="TF-IDF (no length norm)")

    plt.xlabel("Document Length", fontsize=12)
    plt.ylabel("Score Component (fixed TF=5)", fontsize=12)
    plt.title("Document Length Normalization in BM25", fontsize=14)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig("length_normalization_comparison.png")

    print(
        "\nVisualization images saved as 'tf_saturation_comparison.png' and 'length_normalization_comparison.png'"
    )


# ==================== MAIN EXECUTION ====================

if __name__ == "__main__":
    print("=" * 80)
    print("COMPARING BM25 AND TF-IDF RETRIEVAL ALGORITHMS")
    print("=" * 80)

    # Set of queries that highlight different aspects of the algorithms
    queries = [
        "fox dog",  # Basic multi-term query
        "quick brown fox",  # Query with multiple matching terms
        "loyal companion animals",  # Query with conceptual matching
        "wolves",  # Term not directly in corpus but related
        "the the the fox fox",  # Query with repeated terms to show term saturation
    ]

    # Run comparison for each query
    for query in queries:
        run_comparison(query)

    # Generate visualizations
    visualize_algorithm_differences()

    # Demonstration of the effect of document length
    print("\n" + "=" * 80)
    print("DEMONSTRATION OF DOCUMENT LENGTH EFFECTS")
    print("=" * 80)

    # Create a special document collection with varying lengths
    length_test_docs = [
        "fox",  # Very short document
        "fox dog quick",  # Short document
        "fox dog quick brown lazy jumps",  # Medium document
        "fox " * 20,  # Long document with repeated "fox"
        "fox dog " * 15,  # Long document with repeated "fox dog"
        "The fox and the dog were in the forest. " * 5,  # Very long document
    ]

    query = "fox dog"

    print(f"\nQuery: '{query}'")
    print("\nDocument Collection:")
    for i, doc in enumerate(length_test_docs):
        print(
            f"Document {i}: {doc[:50]}{'...' if len(doc) > 50 else ''} (Length: {len(doc.split())} words)"
        )

    # TF-IDF Results
    tfidf_results = calculate_tf_idf_sklearn(length_test_docs, query)
    print("\nTF-IDF Results:")
    for i, (doc_idx, score) in enumerate(tfidf_results):
        doc_preview = length_test_docs[doc_idx][:50] + (
            "..." if len(length_test_docs[doc_idx]) > 50 else ""
        )
        print(f"{i + 1}. [{score:.4f}] Document {doc_idx}: {doc_preview}")

    # BM25 Results with different b values
    for b in [0, 0.5, 0.75, 1.0]:
        bm25_results = calculate_bm25(length_test_docs, query, b=b)
        print(f"\nBM25 Results (k1=1.5, b={b}):")
        for i, (doc_idx, score) in enumerate(bm25_results):
            doc_preview = length_test_docs[doc_idx][:50] + (
                "..." if len(length_test_docs[doc_idx]) > 50 else ""
            )
            print(f"{i + 1}. [{score:.4f}] Document {doc_idx}: {doc_preview}")

    print("\nCONCLUSION:")
    print(
        """
    Key observations from these examples:

    1. TF-IDF tends to favor documents with high term frequency, potentially giving too much weight
       to term repetition and longer documents.

    2. BM25 with appropriate parameters (typically k1=1.2-2.0, b=0.75) provides more balanced results
       by incorporating term frequency saturation and document length normalization.

    3. BM25's parameter b controls how much document length affects scoring:
       - b=0: No length normalization (like TF-IDF)
       - b=1: Full length normalization
       - b=0.75: Balanced approach (standard)

    4. BM25's parameter k1 controls term frequency saturation:
       - Lower k1: More aggressive saturation (diminishing returns for term repetition)
       - Higher k1: Less saturation (closer to TF-IDF)

    5. Both algorithms are lexical matching techniques and don't understand:
       - Synonyms (e.g., "canine" vs "dog")
       - Semantic relationships (e.g., "wolf" is related to "dog")
       - Language variations (e.g., plurals, tenses)

    6. For cross-language or semantic matching, embedding-based approaches would be needed instead.
    """
    )
