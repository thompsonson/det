# det/main.py


import typer
from rich.console import Console
from rich.progress import Progress

from det.det_response.analysis import ResponseAnalysis
from det.det_response.presentation import ResponsePresenter
from det.det_response.semantic_distance import SemanticDistanceCalculator
from det.helpers import get_embedding_generator_adapter, get_llm_client, dynamic_import
from det.llm.llm_langchain import LangChainClient

app = typer.Typer()


def parse_input_variables(input_vars_str: str) -> dict:
    """
    Parses a string of comma-separated key=value pairs into a dictionary.
    """
    return dict(pair.split("=") for pair in input_vars_str.split(","))


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
        for _ in progress.track(range(iterations), description="Processing..."):
            response = lang_chain_client.generate_response()
            responses.append(response)

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

    console.print(analysis.deep_diff_responses(), width=120)

    # Initialize the presenter object with the analysis object
    presenter = ResponsePresenter(analysis, pydantic_object)

    # Call the new method to display the differences in a table format
    deep_diff_output = analysis.deep_diff_responses()
    presenter.display_deep_diff_table(deep_diff_output)


if __name__ == "__main__":
    app()
