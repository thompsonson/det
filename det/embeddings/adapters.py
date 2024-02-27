"""
Embeddings Adapter Module

# embeddings/adapters.py

This module provides a collection of adapter classes that implement the EmbeddingGeneratorInterface
to generate text embeddings using various external services or models, with an emphasis on
extensibility and caching capabilities to enhance performance.

The adapters act as intermediaries between the abstract interface and concrete embedding generation
mechanisms, allowing for flexible integration of different embedding sources without modifying
client code. This modular approach simplifies the process of adding new embedding generators or
switching between them.

Example usage:

    from embeddings.adapters import OpenAIEmbeddingGeneratorAdapter

    # Initialize the adapter with a specific model
    embedding_adapter = OpenAIEmbeddingGeneratorAdapter(model="text-embedding-ada-002")

    # Generate embeddings for a list of texts
    embeddings = embedding_adapter.generate_embeddings(["Sample text for embedding."])

    print(embeddings)
    # The adapter utilizes an internal cache to store and retrieve embeddings, reducing
    # the number of external requests and speeding up the process for repeated inputs.

Classes:
    - EmbeddingGeneratorInterface: An abstract base class defining the contract for
        embedding generators.
    - OpenAIEmbeddingGeneratorAdapter: An adapter for the OpenAI Embedding Generator,
        with caching support.
    - AnotherEmbeddingGenerator: A template for additional embedding generator implementations.

The module demonstrates the use of the Adapter Design Pattern to facilitate the interaction between
high-level operations and external libraries or APIs. It ensures that changes in the embedding
generation services have minimal impact on the application code, promoting maintainability
and scalability.

"""


from abc import ABC, abstractmethod

from det.embeddings.cache import EmbeddingsCache
from det.embeddings.generator import OpenAIEmbeddingGenerator


class EmbeddingGeneratorInterface(ABC):
    @abstractmethod
    def generate_embeddings(self, texts):
        pass


class OpenAIEmbeddingGeneratorAdapter(EmbeddingGeneratorInterface):
    def __init__(self, model="text-embedding-ada-002"):
        self.embedding_generator = OpenAIEmbeddingGenerator(model=model)
        self.embeddings_cache = EmbeddingsCache(
            embeddings_generator=self.embedding_generator
        )

    def generate_embeddings(self, texts):
        return self.embeddings_cache.generate_embeddings(texts)


class AnotherEmbeddingGenerator(EmbeddingGeneratorInterface):
    def generate_embeddings(self, texts):
        # Implementation for another source of embeddings
        pass
