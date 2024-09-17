# det/main.py

import re
import typer
from rich.console import Console
from rich.progress import Progress

from det.det_response.analysis import ResponseAnalysis
from det.det_response.presentation import ResponsePresenter
from det.det_response.semantic_distance import SemanticDistanceCalculator
from det.helpers import get_embedding_generator_adapter, get_llm_client, dynamic_import
from det.llm.llm_langchain import LangChainClient, ResponseGenerationError

app = typer.Typer()


def parse_input_variables(input_vars_str: str) -> dict:
    """
    Parses a string of key=value pairs into a dictionary.
    Handles cases where values might contain commas.
    """
    result = {}
    current_key = None
    current_value = []

    # Split the string by commas, but only when not inside quotes
    parts = re.split(r',(?=(?:[^"]*"[^"]*")*[^"]*$)', input_vars_str)

    for part in parts:
        if "=" in part:
            if current_key:
                result[current_key] = "".join(current_value).strip()
                current_value = []
            current_key, value = part.split("=", 1)
            current_key = current_key.strip()
            current_value.append(value)
        else:
            current_value.append("," + part)

    if current_key:
        result[current_key] = "".join(current_value).strip()

    # Remove any surrounding quotes from values
    for key, value in result.items():
        if value.startswith('"') and value.endswith('"'):
            result[key] = value[1:-1]

    return result


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
    """
    Check the consistency of responses from a language model.

    This command generates multiple responses using the specified LLM and analyzes
    their semantic similarity. It's useful for assessing the determinism and
    consistency of language model outputs.
    """

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
    presenter = ResponsePresenter(analysis, None)
    presenter.display_responses_and_differences_table()


@app.command()
def check_chain(
    iterations: int = typer.Option(10, help="Number of iterations to check responses"),
    prompt_config: str = typer.Option(
        ...,
        help="Custom path to the prompts.json configuration file.",
    ),
    prompt_group: str = typer.Option(..., help="Prompt group, e.g., 'RiskEnrichment'"),
    input_variables_str: str = typer.Option(
        ..., help="Input variables as a comma-separated list of key=value pairs"
    ),
    embeddings_provider: str = typer.Option(
        ..., help="Embeddings provider, e.g., 'OpenAI'"
    ),
    embeddings_model: str = typer.Option(
        ..., help="Embeddings model, e.g., 'text-embedding-ada-002'"
    ),
):
    """
    Run a LangChain-based Structured Output prompt chain and analyze the consistency of responses.

    This command executes a specified prompt chain multiple times, generating
    structured responses based on the provided configuration. It then analyzes
    the semantic similarity between these responses to assess consistency.
    """

    responses = []
    console = Console()

    # Ensure input_variables are parsed and used to configure the LangChainClient
    input_variables = parse_input_variables(input_variables_str)

    lang_chain_client = LangChainClient(prompts_file_path=prompt_config)
    lang_chain_client.configure_chain(
        prompt_group=prompt_group,
        input_variables=input_variables,
    )

    with Progress() as progress:
        for iteration in progress.track(range(iterations), description="Processing..."):
            try:
                response = lang_chain_client.generate_response()
                responses.append(response)
            except ResponseGenerationError:
                console.print(
                    f"[bold red]Warning![/bold red] Failed to get a valid response for iteration [bold yellow]{iteration + 1}[/bold yellow]"
                )

    console.print("The first response:", style="bold underline")
    console.print(responses[0])

    # Dynamic selection of the embedding generator based on the provider
    embedding_generator_adapter = get_embedding_generator_adapter(
        embeddings_provider, embeddings_model
    )

    # Initialize the SemanticDistanceCalculator with the adapter
    semantic_distance_calculator = SemanticDistanceCalculator(
        embedding_generator=embedding_generator_adapter
    )

    analysis = ResponseAnalysis(responses, semantic_distance_calculator)
    # console.print(analysis.deep_diff_responses(), width=120)

    pydantic_object = None

    prompts = lang_chain_client.prompt_manager.get_prompts(prompt_group)
    output_parser_config = prompts.get("outputparser", {})
    pydantic_model_path = output_parser_config.get("value", "")

    # Dynamically load the Pydantic model if specified
    if pydantic_model_path:
        pydantic_object = dynamic_import(pydantic_model_path)

    # Initialize the presenter object with the analysis object
    presenter = ResponsePresenter(analysis, pydantic_object)

    # Analyse the responses and then present the similarty scores
    analysis.deep_diff_responses()
    presenter.display_semantic_similarity_table()


if __name__ == "__main__":
    app()
