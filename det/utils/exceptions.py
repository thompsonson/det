"exceptions for this project"


class LLMInitialisationError(Exception):
    """Raised when an LLM provider cannot be initialized."""


class LLMCommunicationError(Exception):
    """Raised when there's a communication problem with the LLM provider."""


class LLMPromptError(Exception):
    """Raised when there's an issue with the prompts."""


class NVDCommunicationError(Exception):
    """Raised when there's an issue getting the NVD data."""
