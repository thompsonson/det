# det/llm/base.py

from abc import ABC, abstractmethod


class LLMGeneratorInterface(ABC):
    """
    Base class for LLM clients.

    Example Usage:
    --------------
    class MyLLMClient(BaseLLMClient):
        def __init__(self, **kwargs):
            # Initialize any necessary variables or state
            pass

        def generate_response(self, prompt: str, **kwargs) -> str:
            # Implementation for a specific LLM provider
            pass
    """

    def __init__(self, **kwargs):
        # Initialize any necessary variables or state
        pass

    @abstractmethod
    def generate_response(self, prompt: str, **kwargs) -> str:
        """
        Generates a response to a given prompt using the LLM.

        :param prompt: The input prompt to generate text for.
        :param kwargs: Additional parameters specific to the LLM provider.
            - `temperature`: default is 0.
            - `max_tokens`: default is 256.
        :return: The generated text response.
        """
        pass


class ResponseGenerationError(Exception):
    pass
