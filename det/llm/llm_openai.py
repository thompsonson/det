"""
# llm/llm_openai.py

This module defines the OpenAIClient class, an implementation of the BaseLLMClient for generating
text responses using OpenAI's API. It abstracts the details of API interaction, allowing for easy
generation of text completions with various configurations.

The client utilizes environment variables for API authentication, ensuring secure access without
hard-coding sensitive information. It supports specifying a model at initialization for all
subsequent requests, with the option to override default parameters per request.

Example:
--------
    llm_client = OpenAIClient(model="text-davinci-003")
    prompt = "Explain the significance of abstract classes in object-oriented programming."
    response = llm_client.generate_response(prompt, temperature=0.5, max_tokens=100)
    print(response)

This setup facilitates seamless integration with different Large Language Models by adhering to the
BaseLLMClient interface, promoting a plug-and-play architecture for text generation tasks.
"""

from openai import OpenAI
import openai 
import logging 

from det.llm.base import LLMGeneratorInterface
logger = logging.getLogger(__name__)


class OpenAIClient(LLMGeneratorInterface):
    """
    Example:
    --------
        llm_client = OpenAIClient(model="text-davinci-003", api_key="your_api_key_here")
        prompt = "Explain the significance of abstract classes in object-oriented programming."
        response = llm_client.generate_response(prompt, temperature=0.5, max_tokens=100)
        print(response)
    """

    def __init__(self, model: str = "gpt-3.5-turbo", api_key: str = None):
        try:
            if api_key:
                self.client = OpenAI(api_key=api_key)
                logger.info("OpenAI client instantiated successfully using api_key.")
            else:
                self.client = OpenAI()
                logger.info("OpenAI client instantiated successfully without api_key.")
            self.model = model
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
