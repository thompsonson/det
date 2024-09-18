# tests/unit/conftest.py

import logging
import os
import tempfile
from unittest.mock import create_autospec, patch

import pytest

from det.embeddings.adapters import OpenAIEmbeddingGeneratorAdapter
from det.embeddings.cache import EmbeddingsCache
from det.embeddings.generator import EmbeddingGenerator, OpenAIEmbeddingGenerator

logging.basicConfig(level=logging.DEBUG)


@pytest.fixture
def sample_texts():
    """Fixture for providing sample texts."""
    return ["Sample text for embedding."]


@pytest.fixture
def expected_embeddings():
    """Fixture for providing expected embeddings for the sample texts."""
    return [[0.1, 0.2, 0.3]]  # Simplified example of embeddings


@pytest.fixture
def sample_texts_multiple():
    """Fixture for providing multiple sample texts."""
    return ["Text 1", "Text 2"]


@pytest.fixture
def expected_embeddings_multiple():
    """Fixture for providing expected embeddings for multiple sample texts."""
    return [[0.1, 0.2], [0.3, 0.4]]


@pytest.fixture
def mock_openai_embedding_generator():
    """Fixture for creating a mock of OpenAIEmbeddingGenerator."""
    mock = create_autospec(OpenAIEmbeddingGenerator, instance=True)
    mock.generate_embeddings.return_value = [[0.1, 0.2, 0.3]]  # Example embeddings
    return mock


@pytest.fixture
def embedding_generator_interface_mock(mock_openai_embedding_generator):
    """Fixture for an EmbeddingGeneratorInterface mock."""
    return mock_openai_embedding_generator


@pytest.fixture
def openai_embedding_generator_adapter(mocker):
    """Fixture to create an OpenAIEmbeddingGeneratorAdapter with a mocked EmbeddingsCache."""

    def _adapter(expected_embeddings):
        mocker.patch.object(
            EmbeddingsCache, "generate_embeddings", return_value=expected_embeddings
        )
        return OpenAIEmbeddingGeneratorAdapter(
            model="text-embedding-ada-002", api_key="testing"
        )

    return _adapter


@pytest.fixture
def mocked_embedding_generator(mocker, expected_embeddings):
    """Creates a mock EmbeddingGenerator."""
    mock = mocker.create_autospec(EmbeddingGenerator, instance=True)
    mock.generate_embeddings.return_value = expected_embeddings
    return mock


@pytest.fixture
def embeddings_cache_with_mocked_generator(mocked_embedding_generator):
    """Creates an EmbeddingsCache using the mocked EmbeddingGenerator."""
    with tempfile.TemporaryDirectory() as tempdir, patch.object(
        EmbeddingsCache, "_save_cache", return_value=None
    ):
        temp_cache_file = os.path.join(tempdir, "embeddings_cache.pkl")
        # Ensure the file exists and is empty
        open(temp_cache_file, "a").close()

        cache = EmbeddingsCache(
            embeddings_generator=mocked_embedding_generator,
            cache_file_path=temp_cache_file,
        )
        yield cache


@pytest.fixture
def adapter_with_mocked_cache(embeddings_cache_with_mocked_generator):
    adapter = OpenAIEmbeddingGeneratorAdapter(
        model="text-embedding-ada-002", api_key="testing"
    )
    adapter.embeddings_cache = embeddings_cache_with_mocked_generator
    return adapter


@pytest.fixture
def temp_cache_file():
    """Creates a temporary cache file for testing."""
    with tempfile.NamedTemporaryFile(delete=False) as tmpfile:
        yield tmpfile.name
    os.unlink(tmpfile.name)


@pytest.fixture
def mock_openai_api_error(mocker):
    """Mock the OpenAI API to simulate an error."""
    mocker.patch(
        "det.embeddings.generator.OpenAIEmbeddingGenerator.generate_embeddings",
        side_effect=Exception("Simulated API error"),
    )


@pytest.fixture
def empty_texts_fixture():
    """Provides an empty list for testing."""
    return []


@pytest.fixture
def long_text_fixture():
    """Provides a very long text string for testing."""
    return ["Long text " * 1000]


@pytest.fixture
def embeddings_cache_with_faulty_generator(mocker, temp_cache_file):
    """Creates an EmbeddingsCache instance with a faulty mocked EmbeddingGenerator."""
    mock_generator = create_autospec(EmbeddingGenerator, instance=True)
    mock_generator.generate_embeddings.side_effect = Exception(
        "Simulated generator error"
    )
    return EmbeddingsCache(
        embeddings_generator=mock_generator, cache_file_path=temp_cache_file
    )


@pytest.fixture
def mock_openai_api_response(mocker):
    """Mocks responses from the OpenAI API to simulate various scenarios."""
    return mocker.patch(
        "det.embeddings.generator.OpenAIEmbeddingGenerator.generate_embeddings",
        return_value=[[0.1, 0.2, 0.3]],
    )


@pytest.fixture
def adapter_with_faulty_cache(mock_openai_api_error):
    """Fixture to create an OpenAIEmbeddingGeneratorAdapter with a faulty cache."""
    adapter = OpenAIEmbeddingGeneratorAdapter(
        model="text-embedding-ada-002", api_key="testing"
    )
    adapter.embeddings_cache = EmbeddingsCache(
        embeddings_generator=mock_openai_api_error
    )
    return adapter


@pytest.fixture
def expected_long_text_embedding():
    # Example: Generate a placeholder embedding of the correct length
    return [0.0] * 1568  # or any other method of generating a list of this length
import pytest
from pathlib import Path

@pytest.fixture
def resources_dir():
    """Fixture to provide the path to the resources directory."""
    return Path(__file__).parent.parent / "resources"
