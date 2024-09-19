# det/llm/llm_openai_function.py

from openai import OpenAI
from det.llm.base import LLMGeneratorInterface


class OpenAIFunctionClient(LLMGeneratorInterface):
    """
    OpenAIFunctionClient is a class that interacts with OpenAI's API to generate responses
    using function calls. It inherits from LLMGeneratorInterface.
    """

    def __init__(self, model: str = "gpt-3.5-turbo", api_key: str = None):
        if api_key:
            self.client = OpenAI(api_key=api_key)
        else:
            self.client = OpenAI()
        self.model = model

    def generate_response(self, prompt: str, **kwargs) -> str:
        pass

    def generate_response_with_function_call(
        self, messages: list, tools: list, **kwargs
    ) -> dict:
        """
        Generates a response with potential function calls.

        :param messages: List of message dictionaries.
        :param tools: List of available tools/functions.
        :param kwargs: Additional parameters specific to the LLM provider.
        :return: A dictionary containing the response and any function calls.
        """
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                tools=tools,
                **kwargs,
            )

            return response.choices[0].message.tool_calls[0].function
        except Exception as e:
            print(f"An error occurred: {e}")
            return {"response": None, "function_calls": None}
