class MockLLM:
    def __init__(self, response="This is a mock response"):
        self.response = response

    def generate(self, prompt):
        return self.response

    def __call__(self, prompt):
        return self.generate(prompt)


def create_mock_llm(response="This is a mock response"):
    return MockLLM(response)
