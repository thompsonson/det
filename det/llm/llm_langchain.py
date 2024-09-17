# det/llm/llm_langchain.py

from langchain.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain_core.exceptions import OutputParserException

from det.utils.llm_handler import LLMHandler
from det.utils.prompt_manager import PromptManager
from det.llm.base import LLMGeneratorInterface, ResponseGenerationError
from det.helpers import dynamic_import

from rich.console import Console
from time import sleep

console = Console()


class LangChainClient(LLMGeneratorInterface):
    """
    LangChainClient is a class that represents a client for the LangChain system.
    It is responsible for configuring the language learning model (LLM) chain and
    generating responses based on user input.

    Example Usage:
        client = LangChainClient()
        client.configure_chain(
            prompt_group="example_prompt_group",
            input_variables={"name": "John"}
        )
        response = client.generate_response()

    Note:
        The LangChainClient class requires the LLMHandler and PromptManager classes
          to be imported from the appropriate modules.
    """

    def __init__(self, prompts_file_path=None, max_retries=3):
        self.llm_handler = LLMHandler()
        self.prompt_manager = PromptManager(prompts_file_path=prompts_file_path)
        self.chain = None
        self.input_variables = None
        self.max_retries = max_retries

    def configure_chain(self, prompt_group: str, input_variables: dict, **kwargs):
        """
        Configure the language learning model (LLM) chain based on the provided prompt
          group and input variables.

        Parameters:
        - prompt_group (str): The name of the prompt group to retrieve prompts from.
        - input_variables (dict): A dictionary of input variables to be used in the prompts.
        - **kwargs: Additional keyword arguments for configuring the LLM.

        Raises:
        - ValueError: If the system prompt or user prompt is missing for the specified prompt group.

        Returns:
        - None

        Note:
        - This method sets the 'chain' attribute of the LangChainClient instance.

        Example Usage:
            client = LangChainClient()
            client.configure_chain(
                prompt_group="example_prompt_group",
                input_variables={"name": "John"}
            )
        """
        self.input_variables = input_variables

        prompts = self.prompt_manager.get_prompts(prompt_group)
        output_parser_config = prompts.get("outputparser", {})
        pydantic_model_path = output_parser_config.get("value", "")
        pydantic_object = None

        # Dynamically load the Pydantic model if specified
        if pydantic_model_path:
            pydantic_object = dynamic_import(pydantic_model_path)

        # Dynamically load and instantiate the output parser
        output_parser_type_path = output_parser_config.get("type", "")
        output_parser = None
        if output_parser_type_path:
            output_parser = dynamic_import(output_parser_type_path, pydantic_object)

        format_instructions = (
            output_parser.get_format_instructions()
            if output_parser
            else kwargs.get("format_instructions", None)
        )

        # Attempt to retrieve the prompts
        system_prompt = prompts.get("system_prompt")
        user_prompt = prompts.get("prompt")

        # Check if either prompt is missing and raise an exception if so
        if system_prompt is None:
            raise ValueError(f"System prompt for '{prompt_group}' not found.")
        if user_prompt is None:
            raise ValueError(f"User prompt for '{prompt_group}' not found.")

        prompt = ChatPromptTemplate(
            messages=[
                SystemMessagePromptTemplate.from_template(system_prompt),
                HumanMessagePromptTemplate.from_template(user_prompt),
            ],
            output_parser=output_parser,
            input_variables=list(input_variables.keys()),
            partial_variables={
                **input_variables,
                **(
                    {"format_instructions": format_instructions}
                    if format_instructions
                    else {}
                ),
            },
        )

        llm_model_config = prompts.get("model", {})
        llm = self.llm_handler.get_llm(
            llm_provider=llm_model_config.get("provider"),
            llm_model=llm_model_config.get("model"),
            temperature=llm_model_config.get("temperature", 0.01),
            max_tokens=llm_model_config.get("max_tokens", 256),
            **kwargs,
        )

        # Prepare the initial part of the chain with prompt and LLM
        self.chain = prompt | llm

        # If an output_parser is defined, extend the chain to include it
        if output_parser is not None:
            self.chain |= output_parser

    def generate_response(self) -> str:
        """
        Generate a response based on the configured language learning model (LLM)
          chain and input variables.

        Returns:
            str: The generated response.

        Raises:
            ValueError: If the LLM client has not been configured with a chain
              or input variables.
        """
        if self.chain is None or self.input_variables is None:
            raise ValueError(
                "The Langchain client has not been configured with a chain or input variables."
            )
        attempts = 0
        while attempts < self.max_retries:
            try:
                # Try generating the response
                response = self.chain.invoke(self.input_variables)
                return response  # Return if successful
            except OutputParserException as e:
                attempts += 1
                if attempts < self.max_retries:
                    console.print(
                        f"[yellow]Warning: Failed to generate response. Retrying {attempts}/{self.max_retries}...[/yellow]"
                    )
                    sleep(1)  # Optional: Introduce a small delay between retries
                else:
                    raise ResponseGenerationError(
                        f"Failed after {self.max_retries} attempts: {str(e)}"
                    )
