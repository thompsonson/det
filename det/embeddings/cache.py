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
import logging
import os
import pickle


from det.embeddings.generator import EmbeddingGeneratorInterface

logger = logging.getLogger(__name__)


class EmbeddingsCache:
    def __init__(
        self,
        embeddings_generator: EmbeddingGeneratorInterface,
        cache_file_path,
    ):
        self.cache_file_path = (
            cache_file_path if cache_file_path else "embeddings_cache.pkl"
        )
        self.embeddings_generator = (
            embeddings_generator  # Directly use the passed embeddings generator
        )
        self.embeddings_cache = self._load_cache()
        atexit.register(self._save_cache)

    def _load_cache(self):
        """Load the cache from a file if it exists, otherwise return an empty dictionary."""
        logger.debug(f"Attempting to load cache from: {self.cache_file_path}")
        if os.path.exists(self.cache_file_path):
            try:
                with open(self.cache_file_path, "rb") as cache_file:
                    cache = pickle.load(cache_file)
                    logger.info(
                        f"Cache loaded successfully from: {self.cache_file_path}"
                    )
                    return cache
            except EOFError:
                logger.warning(
                    f"Cache file exists but is empty: {self.cache_file_path}"
                )
                return {}
        else:
            logger.info(f"Cache file does not exist: {self.cache_file_path}")
            return {}

    def generate_embeddings(self, texts):
        """Generate embeddings for a list of texts, using cached results where available."""
        embeddings_to_return = []
        texts_without_embeddings = []

        for text in texts:
            if text in self.embeddings_cache:
                logger.debug("Cache hit for text.")
                embeddings_to_return.append(self.embeddings_cache[text])
            else:
                logger.debug("Cache miss for text.")
                texts_without_embeddings.append(text)

        if texts_without_embeddings:
            new_embeddings = self.embeddings_generator.generate_embeddings(
                texts_without_embeddings
            )
            for text, embedding in zip(texts_without_embeddings, new_embeddings):
                self.embeddings_cache[text] = embedding
                logger.debug("Added new embeddings to cache")
                embeddings_to_return.append(embedding)

        return embeddings_to_return

    def _save_cache(self):
        """Save the current state of the cache to a file."""
        with open(self.cache_file_path, "wb") as cache_file:
            pickle.dump(self.embeddings_cache, cache_file)
