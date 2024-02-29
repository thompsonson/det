# det/embeddings/generator.py

from abc import ABC, abstractmethod
from typing import List

from openai import OpenAI


class EmbeddingGeneratorInterface(ABC):
    """
    An abstract base class defining the contract for embedding generators.
    """

    @abstractmethod
    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a list of texts.

        :param texts: A list of strings for which to generate embeddings.
        :return: A list of embeddings for each input text.
        """
        pass


class EmbeddingGenerator(EmbeddingGeneratorInterface):
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


class OpenAIEmbeddingGenerator(EmbeddingGeneratorInterface):
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


class AnotherEmbeddingGenerator(EmbeddingGeneratorInterface):
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
