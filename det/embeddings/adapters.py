from abc import ABC, abstractmethod
from typing import List
import logging

from det.embeddings.cache import EmbeddingsCache
from det.embeddings.generator import (
    EmbeddingGeneratorInterface,
    OpenAIEmbeddingGenerator,
)

logger = logging.getLogger(__name__)


class EmbeddingGeneratorAdapterInterface(ABC):
    def __init__(self, model: str):
        self.model = model
        self.embedding_generator: EmbeddingGeneratorInterface = (
            self._create_embedding_generator()
        )

    @abstractmethod
    def _create_embedding_generator(self) -> EmbeddingGeneratorInterface:
        pass

    @abstractmethod
    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        pass


class OpenAIEmbeddingGeneratorAdapter(EmbeddingGeneratorAdapterInterface):
    def __init__(
        self,
        model: str = "text-embedding-ada-002",
        embedding_generator: EmbeddingGeneratorInterface = None,
        cache_file_path: str = None,
        api_key: str = None,
    ):
        """
        Initializes the OpenAIEmbeddingGeneratorAdapter instance.

        Args:
            model (str): The model to use for generating embeddings.
            embedding_generator (EmbeddingGeneratorInterface): The instance of the EmbeddingGeneratorInterface used for generating embeddings.
            cache_file_path (str): The file path to save the cache.
            api_key (str): The API key for accessing OpenAI's API.
        """
        # Allow passing a specific embedding_generator; otherwise, use the default
        self.embedding_generator = embedding_generator or OpenAIEmbeddingGenerator(
            model=model, api_key=api_key
        )

        self.embeddings_cache = EmbeddingsCache(
            embeddings_generator=self.embedding_generator,
            cache_file_path=cache_file_path,
        )
        # called after setting the embedding_generator up as the super init will call it
        super().__init__(model)

    def _create_embedding_generator(self) -> EmbeddingGeneratorInterface:
        """
        Creates an instance of the OpenAIEmbeddingGenerator class, ensuring it implements the EmbeddingGeneratorInterface.

        Returns:
            EmbeddingGeneratorInterface: The instance of the EmbeddingGeneratorInterface.
        """
        return self.embedding_generator

    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generates embeddings for a list of texts using the EmbeddingsCache and OpenAIEmbeddingGenerator.

        Args:
            texts (List[str]): The list of texts to generate embeddings for.

        Returns:
            List[List[float]]: The generated embeddings.
        """
        return self.embeddings_cache.generate_embeddings(texts)


class AnotherEmbeddingGeneratorAdapter(EmbeddingGeneratorAdapterInterface):
    def __init__(self, model):
        super().__init__(model)
        # Additional setup if necessary

    def _create_embedding_generator(self) -> EmbeddingGeneratorInterface:
        # Return an instance of another class that implements EmbeddingGeneratorInterface
        pass

    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        # Implementation for another source of embeddings
        pass
