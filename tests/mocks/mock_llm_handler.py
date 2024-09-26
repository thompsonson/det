from tests.mocks.mock_llm import MockLLM


class MockLLMHandler:
    def __init__(self, mock_llm=None):
        self.mock_llm = mock_llm or MockLLM()

    def get_llm(
        self, llm_provider=None, llm_model=None, temperature=0.0, max_tokens=1500
    ):
        return self.mock_llm


def create_mock_llm_handler(mock_llm=None):
    return MockLLMHandler(mock_llm)
