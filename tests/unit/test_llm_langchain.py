import pytest
from det.llm.llm_langchain import LangChainClient

def test_langchain_client_initialization():
    """Test the initialization of LangChainClient with default parameters."""
    client = LangChainClient()
    assert client.llm_handler is not None, "LLMHandler should be initialized."
    assert client.prompt_manager is not None, "PromptManager should be initialized."
    assert client.chain is None, "Chain should be None initially."
    assert client.input_variables is None, "Input variables should be None initially."
    assert client.max_retries == 3, "Default max_retries should be 3."
