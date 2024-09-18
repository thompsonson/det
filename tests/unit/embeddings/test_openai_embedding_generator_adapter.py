# tests/unit/embeddings/test_openai_embedding_generator_adapter.py

import pytest


from det.embeddings.adapters import OpenAIEmbeddingGeneratorAdapter


@pytest.mark.parametrize(
    "sample_texts,expected_embeddings",
    [
        (["Sample text for embedding."], [[0.1, 0.2, 0.3]]),  # Single text scenario
        (["Text 1", "Text 2"], [[0.1, 0.2], [0.3, 0.4]]),  # Multiple text scenario
    ],
)
def test_embedding_output(
    openai_embedding_generator_adapter, sample_texts, expected_embeddings
):
    """Test that the adapter correctly handles both single and multiple text inputs."""
    adapter = openai_embedding_generator_adapter(expected_embeddings)
    embeddings = adapter.generate_embeddings(sample_texts)
    assert (
        embeddings == expected_embeddings
    ), "The adapter should return correct embeddings for the provided texts."


def test_consistent_results_for_repeated_inputs(
    embeddings_cache_with_mocked_generator, sample_texts
):
    """Ensure consistent results for repeated inputs, implying deterministic behavior."""
    # First call to generate embeddings should use the mock
    first_result = embeddings_cache_with_mocked_generator.generate_embeddings(
        sample_texts
    )

    # Repeated call with the same texts should yield identical results
    second_result = embeddings_cache_with_mocked_generator.generate_embeddings(
        sample_texts
    )

    # Verify results are identical, implying deterministic output
    assert (
        first_result == second_result
    ), "Expected identical results for repeated inputs, implying deterministic behavior."


def test_cache_efficiency_for_repeated_inputs(
    adapter_with_mocked_cache, sample_texts, mocked_embedding_generator
):
    """
    Test cache efficiency by verifying the EmbeddingGenerator's generate_embeddings method
    is called only once for repeated inputs.
    """
    # Adapter is already configured with a mocked cache and generator in the fixture.
    adapter = adapter_with_mocked_cache

    # Invoke generate_embeddings with the same input twice.
    adapter.generate_embeddings(sample_texts)
    adapter.generate_embeddings(sample_texts)

    # Assert the underlying generator method was called once, proving cache efficiency.
    mocked_embedding_generator.generate_embeddings.assert_called_once_with(sample_texts)


def test_embedding_output_for_empty_input(openai_embedding_generator_adapter):
    """Test how the adapter handles an empty input list."""
    adapter = openai_embedding_generator_adapter([])
    embeddings = adapter.generate_embeddings([])
    assert embeddings == [], "The adapter should return an empty list for empty input."


@pytest.mark.parametrize(
    "long_text", ["This is a very long text input" * 10000], ids=["very_long_text_test"]
)
def test_embedding_output_for_long_text(
    openai_embedding_generator_adapter, long_text, expected_long_text_embedding
):
    """Test the adapter's response to a single long text input."""
    adapter = openai_embedding_generator_adapter(expected_long_text_embedding)
    embeddings = adapter.generate_embeddings([long_text])
    assert (
        embeddings == expected_long_text_embedding
    ), "The adapter should handle long text inputs correctly."


def test_error_handling_on_api_failure(mock_openai_embedding_generator, sample_texts):
    """Test how the adapter handles errors from the underlying API."""
    mock_openai_embedding_generator.generate_embeddings.side_effect = Exception(
        "API failure"
    )
    adapter = OpenAIEmbeddingGeneratorAdapter(
        model="text-embedding-ada-002",
        embedding_generator=mock_openai_embedding_generator,
    )
    with pytest.raises(Exception, match="API failure"):
        adapter.generate_embeddings(sample_texts)


def test_empty_cache_file_handling(
    tmp_path, mock_openai_embedding_generator, sample_texts, expected_embeddings
):
    """Test handling of an existing but empty cache file."""
    # Create an empty cache file
    cache_file_path = tmp_path / "embeddings_cache.pkl"
    open(cache_file_path, "wb").close()  # Create an empty file

    # Initialize the adapter with the empty cache file
    adapter = OpenAIEmbeddingGeneratorAdapter(
        model="text-embedding-ada-002",
        embedding_generator=mock_openai_embedding_generator,
        cache_file_path=str(cache_file_path),
    )

    # Generate embeddings to ensure the adapter functions correctly
    embeddings = adapter.generate_embeddings(sample_texts)
    assert (
        embeddings == expected_embeddings
    ), "The adapter should handle an empty cache file correctly."


def test_cache_creation_on_new_adapter_instance(
    tmp_path, mock_openai_embedding_generator
):
    """Verify that a new cache file is created or an existing one is used when an adapter instance is created."""
    cache_file_path = tmp_path / "embeddings_cache.pkl"
    OpenAIEmbeddingGeneratorAdapter(
        model="text-embedding-ada-002",
        embedding_generator=mock_openai_embedding_generator,
        cache_file_path=str(cache_file_path),
    )
    # Check if the cache file is created
    assert (
        cache_file_path.exists()
    ), "Cache file should be created on adapter initialization."
