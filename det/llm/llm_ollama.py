# det/llm/llm_ollama.py

from abc import ABC, abstractmethod

from ollama import Client

import logging


from det.llm.base import LLMGeneratorInterface


logger = logging.getLogger(__name__)


class OllamaClient(LLMGeneratorInterface):
    """
    The `OllamaClient` class is a subclass of the `BaseLLMClient` abstract class.
    It is used to generate text responses using the Ollama language model (LLM).
    The class initializes with a specified model and host, and provides a method
    to generate a response to a given prompt using the Ollama LLM.
    """

    def __init__(self, model: str = "llama2", host: str = "http://localhost:11434"):
        """
        Initializes the `OllamaClient` class with the specified model and host.

        Parameters:
        - model (str): The specified model for the Ollama LLM.
        - host (str): The host URL for the Ollama LLM.

        Raises:
        - TypeError: If the model or host parameter is not a string.
        """
        if not isinstance(model, str):
            raise TypeError("Model parameter must be a string.")
        if not isinstance(host, str):
            raise TypeError("Host parameter must be a string.")
        self.model = model
        self.client = Client(host=host)

    def generate_response(self, prompt: str, **kwargs) -> str:
        """
        Generates a response to a given prompt using the Ollama LLM.

        Parameters:
        - prompt (str): The prompt for generating the response.
        - **kwargs: Additional parameters specific to the LLM provider.

        Raises:
        - ValueError: If the prompt is not a string.

        Returns:
        - str: The generated text response.
        """
        if not isinstance(prompt, str):
            raise ValueError("Prompt must be a string.")
        try:
            response = self.client.chat(
                model=self.model,  # Use the model specified during initialization
                messages=[{"role": "user", "content": prompt}],
                stream=False,
                options={"temperature": 0},
            )
            return response["message"]["content"]
        except Exception as e:
            logging.error(f"An error occurred: {e}")


class LLMAdapterInterface(ABC):
    """
    Interface for LLM adapters. Defines the contract that all LLM adapters must follow.
    """

    @abstractmethod
    def generate(self, prompt: str, **kwargs):
        """
        Generates a response to a given prompt using the LLM.

        :param prompt: The input prompt to generate text for.
        :param kwargs: Additional parameters specific to the LLM provider.
        :return: The generated text response.
        """
        pass


class OllamaAdapter(LLMAdapterInterface):
    """
    The `OllamaAdapter` class is used to adapt the Ollama LLM to the `LLMClient` interface,
    following the `LLMAdapterInterface`.
    """

    def __init__(self, model: str = "mistral", host: str = "http://localhost:11434"):
        self.model = model
        self.client = Client(host=host)

    def generate(self, prompt: str, **kwargs):
        response = self.client.chat(
            model=self.model,  # Use the model specified during initialization
            messages=[{"role": "user", "content": prompt}],
            stream=False,
            options={"temperature": 0},
        )
        return response.message.content


class OllamaGenerator(LLMGeneratorInterface):
    """
    The `OllamaGenerator` class is a subclass of the `LLMClient` abstract class.
    It uses the `OllamaAdapter` to generate text responses using the Ollama LLM.
    """

    def __init__(self, model: str = "llama2", host: str = "http://localhost:11434"):
        self.adapter = OllamaAdapter(model, host)

    def generate_response(self, prompt: str, **kwargs) -> str:
        return self.adapter.generate(prompt, **kwargs)
