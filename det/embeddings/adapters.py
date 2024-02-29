from abc import ABC, abstractmethod
from typing import List

from det.embeddings.cache import EmbeddingsCache
from det.embeddings.generator import (
    EmbeddingGeneratorInterface,
    OpenAIEmbeddingGenerator,
)


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
        model="text-embedding-ada-002",
        embedding_generator=None,
        cache_file_path=None,
    ):
        super().__init__(model)

        # Allow passing a specific embedding_generator; otherwise, use the default
        self.embedding_generator = (
            embedding_generator
            if embedding_generator
            else OpenAIEmbeddingGenerator(model=model)
        )

        self.embeddings_cache = EmbeddingsCache(
            embeddings_generator=self.embedding_generator,
            cache_file_path=cache_file_path,
        )

    def _create_embedding_generator(self) -> EmbeddingGeneratorInterface:
        # Ensure the OpenAIEmbeddingGenerator class implements EmbeddingGeneratorInterface
        return OpenAIEmbeddingGenerator(model=self.model)

    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
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
