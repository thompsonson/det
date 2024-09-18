import json
import pytest
from unittest.mock import patch
from langchain.prompts.chat import ChatPromptTemplate
from det.utils.prompt_manager import PromptManager
from det.llm.llm_langchain import LangChainClient

def test_langchain_client_initialization(resources_dir):
    """Test the initialization of LangChainClient with default parameters."""
    prompts_file_path = resources_dir / "prompts.json"
    client = LangChainClient(prompts_file_path=prompts_file_path)
    assert client.llm_handler is not None, "LLMHandler should be initialized."
    assert client.prompt_manager is not None, "PromptManager should be initialized."
    assert client.chain is None, "Chain should be None initially."
    assert client.input_variables is None, "Input variables should be None initially."
    assert client.max_retries == 3, "Default max_retries should be 3."
def test_configure_chain_with_valid_prompts(resources_dir):
    """Test configuring the chain with valid prompts and input variables."""
    prompts_file_path = resources_dir / "prompts.json"
    client = LangChainClient(prompts_file_path=prompts_file_path)
    
    input_variables = {"risk_statement": "Sample risk statement"}
    client.configure_chain(prompt_group="RiskDefinition", input_variables=input_variables)
    
    assert client.chain is not None, "Chain should be configured."
    assert client.input_variables == input_variables, "Input variables should be set correctly."

def test_configure_chain_with_invalid_input_variables(resources_dir):
    """Test configuring the chain with invalid input variables."""
    prompts_file_path = resources_dir / "prompts.json"
    client = LangChainClient(prompts_file_path=prompts_file_path)
    
    input_variables = {"invalid_key": "Invalid value"}
    with pytest.raises(KeyError):
        client.configure_chain(prompt_group="RiskDefinition", input_variables=input_variables)

def test_configure_chain_missing_format_instructions(resources_dir):
    """Test configuring the chain when format instructions are missing."""
    prompts_file_path = resources_dir / "prompts.json"
    client = LangChainClient(prompts_file_path=prompts_file_path)
    
    input_variables = {"risk_statement": "Sample risk statement"}
    with patch.object(PromptManager, 'get_prompts', return_value={
        "system_prompt": "System prompt",
        "prompt": "User prompt",
        "outputparser": {}
    }):
        client.configure_chain(prompt_group="RiskDefinition", input_variables=input_variables)
        assert client.chain is not None, "Chain should be configured even without format instructions."

def test_configure_chain_correct_output_parser_configuration(resources_dir):
    """Test that the output parser is configured correctly."""
    prompts_file_path = resources_dir / "prompts.json"
    client = LangChainClient(prompts_file_path=prompts_file_path)
    
    input_variables = {"risk_statement": "Sample risk statement"}
    client.configure_chain(prompt_group="RiskDefinition", input_variables=input_variables)
    
    assert client.chain.output_parser is not None, "Output parser should be configured."

def test_configure_chain_composition(resources_dir):
    """Test that the chain is composed correctly with the prompt and LLM."""
    prompts_file_path = resources_dir / "prompts.json"
    client = LangChainClient(prompts_file_path=prompts_file_path)
    
    input_variables = {"risk_statement": "Sample risk statement"}
    client.configure_chain(prompt_group="RiskDefinition", input_variables=input_variables)
    
    assert isinstance(client.chain, ChatPromptTemplate), "Chain should be a ChatPromptTemplate instance."
    """Test configuring the chain with valid prompts and input variables."""
    prompts_file_path = resources_dir / "prompts.json"
    client = LangChainClient(prompts_file_path=prompts_file_path)
    
    input_variables = {"risk_statement": "Sample risk statement"}
    client.configure_chain(prompt_group="RiskDefinition", input_variables=input_variables)
    
    assert client.chain is not None, "Chain should be configured."
    assert client.input_variables == input_variables, "Input variables should be set correctly."

def test_configure_chain_missing_system_prompt(resources_dir):
    """Test that configuring the chain raises ValueError if system prompt is missing."""
    prompts_file_path = resources_dir / "prompts.json"
    client = LangChainClient(prompts_file_path=prompts_file_path)
    
    with patch.object(PromptManager, 'get_prompts', return_value={"prompt": "User prompt"}):
        with pytest.raises(ValueError, match="System prompt for 'RiskDefinition' not found."):
            client.configure_chain(prompt_group="RiskDefinition", input_variables={})

def test_configure_chain_missing_user_prompt(resources_dir):
    """Test that configuring the chain raises ValueError if user prompt is missing."""
    prompts_file_path = resources_dir / "prompts.json"
    client = LangChainClient(prompts_file_path=prompts_file_path)
    
    with patch.object(PromptManager, 'get_prompts', return_value={"system_prompt": "System prompt"}):
        with pytest.raises(ValueError, match="User prompt for 'RiskDefinition' not found."):
            client.configure_chain(prompt_group="RiskDefinition", input_variables={})
