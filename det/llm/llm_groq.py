"""
# llm/llm_groq.py

This module defines the GroqClient class, an implementation of the BaseLLMClient for generating
text responses using Groq's API. It abstracts the details of API interaction, allowing for easy
generation of text completions with various configurations.

The client utilizes environment variables for API authentication, ensuring secure access without
hard-coding sensitive information. It supports specifying a model at initialization for all
subsequent requests, with the option to override default parameters per request.

Example:
--------
    llm_client = GroqClient(model="llama3-8b-8192")
    prompt = "Explain the significance of abstract classes in object-oriented programming."
    response = llm_client.generate_response(prompt, temperature=0.5, max_tokens=100)
    print(response)

This setup facilitates seamless integration with different Large Language Models by adhering to the
BaseLLMClient interface, promoting a plug-and-play architecture for text generation tasks.
"""

from groq import Groq
import groq
import logging

from det.llm.base import LLMGeneratorInterface

logger = logging.getLogger(__name__)


class GroqClient(LLMGeneratorInterface):
    """
    Example:
    --------
        llm_client = GroqClient(model="llama3-8b-8192", api_key="your_api_key_here")
        prompt = "Explain the significance of abstract classes in object-oriented programming."
        response = llm_client.generate_response(prompt, temperature=0.5, max_tokens=100)
        print(response)
    """

    def __init__(self, model: str = "llama3-8b-8192", api_key: str = None):
        try:
            if api_key:
                self.client = Groq(api_key=api_key)
            else:
                self.client = Groq()
            self.model = model
            self.client.models.list()
        except groq.APIConnectionError as e:
            logger.error(f"The server could not be reached: {e}")
        except groq.RateLimitError as e:
            logger.error(
                f"A 429 status code was received; we should back off a bit: {e}"
            )
        except groq.APIStatusError as e:
            logger.error(f"Another non-200-range status code was received: {e}")
        except Exception as e:
            logger.error(f"Error instantiating Groq client: {str(e)}")
            self.client = None

    def generate_response(self, prompt: str, **kwargs):
        try:
            response = self.client.chat.completions.create(
                model=self.model,  # Use the model specified during initialization
                messages=[{"role": "user", "content": prompt}],
                **kwargs,
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
