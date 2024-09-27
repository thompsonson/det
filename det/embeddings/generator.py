# det/embeddings/generator.py

from abc import ABC, abstractmethod
from typing import List
import logging

from openai import OpenAI
import openai

logger = logging.getLogger(__name__)


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

    def __init__(self, model: str = "text-embedding-ada-002", api_key: str = None):
        """
        Initialize the OpenAI embedding generator.

        :param model: The model to use for generating embeddings.
        :param api_key: The API key for accessing the OpenAI API.
        """
        self.model = model
        self._instantiate_openai_client(api_key)

    def _instantiate_openai_client(self, api_key: str):
        try:
            if api_key:
                self.client = OpenAI(api_key=api_key)
                logger.info("OpenAI client instantiated successfully using api_key.")
            else:
                self.client = OpenAI()
                logger.info("OpenAI client instantiated successfully without api_key.")
            self.client.models.list()
        except openai.APIConnectionError as e:
            logger.error("The server could not be reached")
            logger.error(e.__cause__)  # The original exception
        except openai.RateLimitError as e:
            logger.error("A 429 status code was received; we should back off a bit.")
        except openai.APIStatusError as e:
            logger.error("Another non-200-range status code was received")
            logger.error(e.status_code)
            logger.error(e.response)
        except Exception as e:
            logger.error(f"Error instantiating OpenAI client: {str(e)}")
            self.client = None

    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings using OpenAI's API.

        :param texts: A list of strings for which to generate embeddings.
        :return: A list of embeddings.
        """
        try:
            response = self.client.embeddings.create(input=texts, model=self.model)
            return [embedding.embedding for embedding in response.data]
        except Exception as e:
            logger.error(f"Error generating embeddings: {str(e)}")
            return []


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
