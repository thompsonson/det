"""
Embeddings Cache Class

# embeddings/cache.py

This module provides functionality to generate text embeddings using various embedding models,
with support for caching to improve performance and reduce API calls.

Example usage:

    from embeddings.generator import OpenAIEmbeddingGenerator
    from embeddings.cache import EmbeddingsCache

    # Create an instance of the embedding generator
    embedding_generator = OpenAIEmbeddingGenerator(model = "text-embedding-ada-002")

    # Initialize the embeddings cache with the embedding generator
    embeddings_cache = EmbeddingsCache(embeddings_generator=embedding_generator)

    # Generate embeddings for a list of texts, using cached results where available
    embeddings = embeddings_cache.generate_embeddings(["Hello, world!"])

    print(embeddings)
    # This will automatically save the cache on exit.

The module is designed to be flexible, allowing for the easy integration of different embedding
models by extending the `EmbeddingGenerator` abstract class. The `EmbeddingsCache` class handles
caching of embeddings to disk, loading them as needed to avoid redundant computation and API
requests.
"""


import atexit
import os
import pickle

from det.embeddings.generator import (
    EmbeddingGenerator,
)  # General import for type hinting


class EmbeddingsCache:
    def __init__(
        self,
        embeddings_generator: EmbeddingGenerator,
        cache_file_path="embeddings_cache.pkl",
    ):
        self.cache_file_path = cache_file_path
        self.embeddings_generator = (
            embeddings_generator  # Directly use the passed embeddings generator
        )
        self.embeddings_cache = self._load_cache()
        atexit.register(self._save_cache)

    def _load_cache(self):
        """Load the cache from a file if it exists, otherwise return an empty dictionary."""
        if os.path.exists(self.cache_file_path):
            with open(self.cache_file_path, "rb") as cache_file:
                return pickle.load(cache_file)
        else:
            return {}

    def generate_embeddings(self, texts):
        """Generate embeddings for a list of texts, using cached results where available."""
        embeddings_to_return = []
        texts_without_embeddings = []

        for text in texts:
            if text in self.embeddings_cache:
                embeddings_to_return.append(self.embeddings_cache[text])
            else:
                texts_without_embeddings.append(text)

        if texts_without_embeddings:
            new_embeddings = self.embeddings_generator.generate_embeddings(
                texts_without_embeddings
            )
            for text, embedding in zip(texts_without_embeddings, new_embeddings):
                self.embeddings_cache[text] = embedding
                embeddings_to_return.append(embedding)

        return embeddings_to_return

    def _save_cache(self):
        """Save the current state of the cache to a file."""
        with open(self.cache_file_path, "wb") as cache_file:
            pickle.dump(self.embeddings_cache, cache_file)
