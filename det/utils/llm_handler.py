" LLM factory "
import logging
from langchain_openai import ChatOpenAI
from langchain_community.chat_models import (
    ChatAnthropic,
    ChatVertexAI,
)
from .exceptions import LLMInitialisationError


class LLMHandler:
    """
    A class to handle the creation and initialization of Language Learning Models.
    """

    LLM_CLASSES = {
        "AzureChatOpenAI": "_create_azure_chat_openai",
        "ChatAnthropic": "_create_chat_anthropic",
        "ChatGoogleVertex": "_create_chat_google_vertex",
        "ChatGooglePaLM": "_create_chat_google_palm",
        "ChatOpenAI": "_create_chat_openai",
    }

    def __init__(self):
        """Initialize the logger for the LLMHandler class."""
        self.logger = logging.getLogger(__name__)

    def _create_chat_openai(self, llm_model, max_tokens, temperature):
        return ChatOpenAI(
            model_name=llm_model, max_tokens=max_tokens, temperature=temperature
        )

    # pylint: disable=W0613
    def _create_chat_anthropic(self, llm_model, max_tokens, temperature):
        return ChatAnthropic(
            max_tokens_to_sample=int(max_tokens), temperature=temperature
        )

    # pylint: disable=W0613
    def _create_chat_google_vertex(self, llm_model, max_tokens, temperature):
        if llm_model == "":
            llm_model = "chat-bison"
        return ChatVertexAI(model_name=llm_model)

    # pylint: disable=W0613
    def _create_chat_google_palm(self, llm_model, max_tokens, temperature):
        raise NotImplementedError("ChatGooglePaLM is not yet implemented.")

    # pylint: disable=W0613
    def _create_azure_chat_openai(self, llm_model, max_tokens, temperature):
        raise NotImplementedError("AzureChatOpenAI is not yet implemented.")

    def get_llm(
        self,
        llm_provider: str,
        llm_model: str = "",
        temperature: float = 0.0,
        max_tokens: int = 1500,
    ):
        """
        Initialize a Language Learning Model (LLM) based on the provided parameters.

        Parameters:
        -----------
        llm_provider: str - The LLM provider.
        llm_model: str - The LLM model name.
        temperature: float - The temperature for generating output.
        max_tokens: int - The maximum number of tokens in the generated output.

        Returns:
        --------
        An initialized LLM.

        Raises:
        -------
        LLMInitialisationError: If an error occurs during the LLM initialization.
        """
        self.logger.info("Initializing %s...", llm_provider)
        try:
            llm = getattr(self, self.LLM_CLASSES[llm_provider])(
                llm_model, max_tokens, temperature
            )
        except Exception as exc:
            self.logger.error("Failed to initialize %s: %s", llm_provider, exc)
            raise LLMInitialisationError(
                f"Failed to initialize {llm_provider}: {exc}"
            ) from exc

        self.logger.info("Successfully initialized %s", llm_provider)

        return llm

    @classmethod
    def get_supported_llm_providers(cls):
        """
        Returns the supported LLM providers.

        Returns:
        -------
        List[str]: A list of supported LLM providers.
        """
        return list(cls.LLM_CLASSES.keys())
