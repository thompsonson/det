# main.py

import typer
from rich.console import Console
from rich.progress import Progress

from det.det_response.analysis import ResponseAnalysis
from det.det_response.presentation import ResponsePresenter
from det.det_response.semantic_distance import SemanticDistanceCalculator
from det.helpers import get_embedding_generator_adapter, get_llm_client

app = typer.Typer()


@app.command()
def check_responses(
    iterations: int = typer.Option(10, help="Number of iterations to check responses"),
    llm_provider: str = typer.Option(..., help="LLM provider, e.g., 'OpenAI'"),
    llm_model: str = typer.Option(..., help="LLM model, e.g., 'gpt-3.5-turbo'"),
    embeddings_provider: str = typer.Option(
        ..., help="Embeddings provider, e.g., 'OpenAI'"
    ),
    embeddings_model: str = typer.Option(
        ..., help="Embeddings model, e.g., 'text-embedding-ada-002'"
    ),
):
    responses = []
    console = Console()

    # get the LLM client
    client = get_llm_client(llm_provider, llm_model)

    # Dynamic selection of the embedding generator based on the provider
    embedding_generator_adapter = get_embedding_generator_adapter(
        embeddings_provider, embeddings_model
    )

    # Initialize the SemanticDistanceCalculator with the adapter
    semantic_distance_calculator = SemanticDistanceCalculator(
        embedding_generator=embedding_generator_adapter
    )

    with Progress() as progress:
        for _ in progress.track(range(iterations), description="Processing..."):
            response = client.generate_response(
                prompt="This is a test of determinism. Will you always respond the same?",
                temperature=0,
                max_tokens=256,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
            )
            responses.append(response)

    console.print("The first response:", style="bold underline")
    console.print(responses[0])

    analysis = ResponseAnalysis(responses, semantic_distance_calculator)
    presenter = ResponsePresenter(analysis)
    presenter.display_responses_and_differences_table()


if __name__ == "__main__":
    typer.run(check_responses)
