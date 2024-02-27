"""
Embedding Generators Module

# embeddings/generator.py

This module offers a flexible approach to generating text embeddings, allowing for easy integration
and use of various embedding models, including OpenAI's API. It is designed to support extensible
embedding generation strategies through the use of an abstract base class and concrete
implementations.

Example usage:

    from embeddings.generator import OpenAIEmbeddingGenerator

    # Initialize the embedding generator with an optional model specification
    embedding_generator = OpenAIEmbeddingGenerator(model="text-embedding-ada-002")

    # Generate embeddings for a list of texts
    embeddings = embedding_generator.generate_embeddings(["Hello, world!", "How are you?"])
    print(embeddings)

The module provides the `EmbeddingGenerator` abstract base class to define a common interface for
all embedding generators. Implementations of this class, such as `OpenAIEmbeddingGenerator`, use
specific APIs or models to generate embeddings. This structure allows for easy extension to include
more generators based on different services or custom embedding models.

Classes:
- `EmbeddingGenerator`: An abstract base class for embedding generators. It requires
  the implementation of a `generate_embeddings` method.
- `OpenAIEmbeddingGenerator`: A concrete implementation of `EmbeddingGenerator` that
  utilizes OpenAI's API to produce embeddings. It allows specifying the model to be
  used.
- `AnotherEmbeddingGenerator`: A placeholder for additional embedding generator
  implementations, showcasing the module's extensibility.

This module is designed with flexibility and extensibility in mind, enabling developers to
seamlessly integrate different embedding generation techniques and models as required by their
applications.
"""


from abc import ABC, abstractmethod
from typing import List

from openai import OpenAI


class EmbeddingGenerator(ABC):
    """
    Abstract base class for embedding generators.
    """

    @abstractmethod
    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a list of texts.

        :param texts: A list of strings for which to generate embeddings.
        :return: A list of embeddings.
        """
        raise NotImplementedError("This method should be implemented by subclasses.")


class OpenAIEmbeddingGenerator(EmbeddingGenerator):
    """
    Embedding generator using OpenAI's API.
    """

    def __init__(self, model: str = "text-embedding-ada-002"):
        """
        Initialize the OpenAI embedding generator.

        :param model: The model to use for generating embeddings.
        """
        self.model = model
        self.client = OpenAI()

    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings using OpenAI's API.

        :param texts: A list of strings for which to generate embeddings.
        :return: A list of embeddings.
        """
        response = self.client.embeddings.create(input=texts, model=self.model)
        return [embedding.embedding for embedding in response.data]


class AnotherEmbeddingGenerator(EmbeddingGenerator):
    """
    Placeholder class for another embedding generator.
    """

    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings using another model.

        :param texts: A list of strings for which to generate embeddings.
        :return: A list of embeddings.
        """
        # Placeholder for implementation
        pass
