"""
Response Presentation Module

# det_response/presentation.py

This module defines the ResponsePresenter class, which leverages the rich library to display
analysis results from the ResponseAnalysis class in an intuitive and visually appealing manner.
It provides methods to display response counts, differences, and semantic similarities in tabular
formats, enhancing readability and insights for users.

The class is particularly useful for presenting analysis results of textual responses, such as those
from chatbots, customer feedback, or any text analysis application, in a clear and structured way.

Example usage:

    from det_response.presentation import ResponsePresenter
    from det_response.analysis import ResponseAnalysis
    from det_response.semantic_distance import SemanticDistanceCalculator

    # Assuming responses have been analyzed with ResponseAnalysis
    responses = ["Hello, how can I assist you today?", ...]
    semantic_distance_calculator = SemanticDistanceCalculator()
    analysis = ResponseAnalysis(responses, semantic_distance_calculator)

    # Initialize the presenter with the analysis
    presenter = ResponsePresenter(analysis)

    # Display a table of response counts, differences, and semantic similarities
    presenter.display_responses_and_differences_table()

    # Display just the response counts
    presenter.display_response_counts()

    # Display character-level differences from the base response
    presenter.display_differences_char()

    # Display word-level differences from the base response
    presenter.display_differences_words()

Key Features:
    - Visual presentation of response counts, highlighting the frequency of each unique response.
    - Detailed display of character-level and word-level differences, with added words highlighted
        for quick identification.
    - Presentation of semantic similarity scores in a table, allowing for a quick overview of how
        closely related the responses are semantically.

This module utilizes the rich library's capabilities to create tables, apply text styles, and manage
console output, making the data more accessible and understandable to users. It's an essential tool
for anyone looking to present textual analysis results in a professional and engaging format.

"""

from rich.console import Console
from rich.table import Table
from rich.text import Text

from det.det_response.analysis import ResponseAnalysis


class ResponsePresenter:
    def __init__(self, analysis: ResponseAnalysis, model_class):
        self.analysis = analysis
        self.console = Console()
        self.model_class = model_class

    def display_responses_and_differences_table(self):
        table = Table(title="Response Counts, Differences, and Semantic Similarity")
        table.add_column("Count", justify="right")
        table.add_column("Differences", justify="left")
        table.add_column("Semantic Similarity", justify="center")

        # Assume the analysis object has a method or property to get the base response
        base_response = self.analysis.base_response
        base_words = base_response.split()

        # And a method or property to get the response counts
        response_counts = self.analysis.response_counts

        # Retrieve semantic similarities
        semantic_similarities = self.analysis.calculate_semantic_similarities()

        for i, (response, count) in enumerate(response_counts.items()):
            current_words = response.split()
            diff_text = Text()

            added_words = set(current_words) - set(base_words)

            for word in current_words:
                if word in added_words:
                    diff_text.append(word, style="green")
                else:
                    diff_text.append(word)
                diff_text.append(" ")

            # Note: This assumes the order of similarities matches the order
            #    of responses in response_counts.
            similarity_score = (
                f"{semantic_similarities[i]:.2f}" if semantic_similarities else "N/A"
            )

            table.add_row(str(count), diff_text, similarity_score)

        self.console.print(table)

    def display_response_counts(self):
        response_counts = self.analysis.group_and_count_responses()
        table = Table(title="Response Counts")
        table.add_column("Count", justify="right")
        table.add_column("Response", justify="left", no_wrap=False)

        for response, count in response_counts.items():
            table.add_row(str(count), response)

        self.console.print(table)

    def display_differences_char(self):
        comparisons = self.analysis.highlight_differences_char()
        for i, diff in enumerate(comparisons):
            diff_text = Text()
            for piece in diff:
                if piece.startswith("+"):
                    diff_text.append(piece[2:], "green")
                else:
                    diff_text.append(piece[2:])
            self.console.print(
                f"Response #{i} compared to Response #0:", style="bold underline"
            )
            self.console.print(diff_text)

    def display_differences_words(self):
        comparisons = self.analysis.highlight_differences_words()
        for i, (current_words, added_words) in enumerate(comparisons):
            diff_text = Text()
            for word in current_words:
                if word in added_words:
                    diff_text.append(word, "green")
                else:
                    diff_text.append(word)
                diff_text.append(" ")
            self.console.print(
                f"Response #{i} compared to Response #0:", style="bold underline"
            )
            self.console.print(diff_text)

    def display_semantic_similarity_table(self):
        similarities = self.analysis.calculate_field_similarities()
        table = Table(title="Semantic Similarity Scores")
        table.add_column("Field", style="cyan")
        for i in range(len(self.analysis.responses)):
            table.add_column(f"i {i+1}", justify="center")

        for field, scores in similarities.items():
            row = [field]
            for score in scores:
                # format the score
                if f"{score:.2f}" <= "0.90":
                    formatted_score = f"[bold red]{score:.2f}[/bold red]"
                elif f"{score:.2f}" <= "0.95":
                    formatted_score = f"[red]{score:.2f}[/red]"
                elif f"{score:.2f}" <= "0.98":
                    formatted_score = f"[magenta]{score:.2f}[/magenta]"
                else:
                    formatted_score = f"[green]{score:.2f}[/green]"

                row.append(formatted_score)

            table.add_row(*row)

        self.console.print(table)
