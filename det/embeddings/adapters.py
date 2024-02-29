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
    def __init__(self, model="text-embedding-ada-002"):
        super().__init__(model)
        self.embeddings_cache = EmbeddingsCache(
            embeddings_generator=self.embedding_generator
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
