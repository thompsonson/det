"""
Semantic Distance Calculation Module

# det_response/semantic_distance.py

This module defines the SemanticDistanceCalculator class, which provides functionality to calculate
the semantic similarity between texts. It utilizes embeddings generated by a specified embedding
generator and calculates cosine similarity between these embeddings to quantify semantic closeness.

The class is essential for applications that require understanding the semantic similarity between
various pieces of text, such as comparing user responses, analyzing text for similarity,
or clustering documents based on content similarity.

Example usage:

    from det_response.semantic_distance import SemanticDistanceCalculator
    # Assume EmbeddingGenerator is a class that provides a method `generate_embeddings`
    # which takes a list of texts and returns their embeddings as NumPy arrays.
    embedding_generator = EmbeddingGenerator()

    semantic_distance_calculator = SemanticDistanceCalculator(embedding_generator)

    base_text = "How can I help you today?"
    compare_texts = [
        "What assistance do you need?",
        "How can I assist you today?",
        "Good morning, how may I help you?"
    ]

    similarities = semantic_distance_calculator.semantic_similarity(base_text, compare_texts)
    print(similarities)

Key Features:
    - Calculates cosine similarity between text embeddings to measure semantic closeness.
    - Supports comparison of one base text against multiple comparison texts, returning a list of
         similarity scores.
    - Requires an embedding generator for generating text embeddings, making it flexible to use
        with various embedding models.

This module is particularly useful for natural language processing (NLP) tasks that involve semantic
analysis, such as chatbot response evaluation, document similarity checks, or content recommendation
systems. By leveraging the power of text embeddings and cosine similarity, it provides a
straightforward method to quantify the semantic similarity between texts, aiding in the analysis
and understanding of textual data.

"""

import numpy as np


class SemanticDistanceCalculator:
    def __init__(self, embedding_generator):
        self.embedding_generator = embedding_generator

    def calculate_cosine_similarity(self, embedding1, embedding2):
        norm1 = embedding1 / np.linalg.norm(embedding1)
        norm2 = embedding2 / np.linalg.norm(embedding2)
        similarity = np.dot(norm1, norm2)
        return similarity

    def semantic_similarity(self, base_text, compare_texts):
        if isinstance(base_text, str):
            base_text = [base_text]
        if isinstance(compare_texts, str):
            compare_texts = [compare_texts]

        embeddings = self.embedding_generator.generate_embeddings(
            base_text + compare_texts
        )
        base_embedding = embeddings[0]
        similarities = [
            self.calculate_cosine_similarity(base_embedding, emb)
            for emb in embeddings[1:]
        ]
        return similarities
