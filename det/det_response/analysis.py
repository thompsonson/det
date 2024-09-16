"""
Response Analysis Module

# det_response/analysis.py

This module defines the ResponseAnalysis class, which provides methods for analyzing sets of
textual responses. It supports operations such as grouping and counting identical responses,
highlighting character-level and word-level differences between responses, and calculating
semantic similarities using a specified SemanticDistanceCalculator.

The class is designed to be used in scenarios where it's necessary to analyze variations in
textual responses, such as in chatbot output, customer feedback analysis, or any application
where understanding textual variation is crucial.

Example usage:

    from det_response.semantic_distance import SemanticDistanceCalculator
    from response_analysis import ResponseAnalysis

    # Example responses from a chatbot or any text generating system
    responses = [
        "Hello, how can I assist you today?",
        "Hi, how can I help you today?",
        "Hello, how may I assist you today?"
    ]

    # Initialize the semantic distance calculator with a specific model or configuration
    semantic_distance_calculator = SemanticDistanceCalculator()

    # Create a ResponseAnalysis instance with the responses and the calculator
    response_analysis = ResponseAnalysis(responses, semantic_distance_calculator)

    # Group and count identical responses
    print(response_analysis.response_counts)

    # Highlight character-level differences from the base response
    print(response_analysis.highlight_differences_char())

    # Highlight word-level differences from the base response
    print(response_analysis.highlight_differences_words())

    # Calculate semantic similarities between the base response and other responses
    print(response_analysis.semantic_similarities)

Key Features:
    - Efficient grouping and counting of identical responses to identify common patterns
        or outliers.
    - Highlighting differences at both character and word levels to visually compare
        responses and identify variations.
    - Calculating semantic similarities between responses using a custom SemanticDistanceCalculator,
        allowing for a deeper understanding of the textual variations beyond syntactic differences.

This module is particularly useful in applications where text responses from different sources or
iterations need to be analyzed for consistency, variations, or improvement over time. It leverages
both syntactic and semantic analysis to provide a comprehensive overview of textual response
dynamics.

"""

from difflib import ndiff
from deepdiff import DeepDiff

from det.det_response.semantic_distance import SemanticDistanceCalculator


class ResponseAnalysis:
    def __init__(
        self, responses, semantic_distance_calculator: SemanticDistanceCalculator
    ):
        self.responses = responses
        self.base_response = responses[0] if responses else None
        self.response_counts = self.group_and_count_responses()
        self.semantic_distance_calculator = semantic_distance_calculator
        # self.semantic_similarities = self.calculate_semantic_similarities()

    def deep_diff_responses(self):
        diffs = []
        for response in self.responses[1:]:  # Skip the base response
            diff = DeepDiff(
                self.base_response, response, ignore_order=True, verbose_level=1
            )
            diffs.append(diff)
        return diffs

    def group_and_count_responses(self):
        response_counts = {}
        for response in self.responses:
            # Convert the response to a string or another suitable representation
            response_key = str(response)
            if response_key in response_counts:
                response_counts[response_key] += 1
            else:
                response_counts[response_key] = 1
        return response_counts

    def highlight_differences_char(self):
        comparisons = []
        for response in self.responses:
            diff = list(ndiff(self.base_response, response))
            comparisons.append(diff)
        return comparisons

    def highlight_differences_words(self):
        base_words = self.base_response.split() if self.base_response else []
        comparisons = []
        for response in self.responses:
            current_words = response.split()
            added_words = set(current_words) - set(base_words)
            comparisons.append((current_words, added_words))
        return comparisons

    def calculate_semantic_similarities(self):
        if not self.base_response or len(self.responses) < 2:
            return []
        return self.semantic_distance_calculator.semantic_similarity(
            self.base_response, self.responses
        )

    def calculate_field_similarities(self):
        if not self.responses:
            return {}

        similarities = {}
        base_dict = self.base_response.dict()
        for field in base_dict.keys():
            similarities[field] = [1.0]  # First iteration always 1.0
            base_value = str(getattr(self.base_response, field))
            for response in self.responses[1:]:
                compare_value = str(getattr(response, field))
                score = self.semantic_distance_calculator.semantic_similarity(
                    base_value, [compare_value]
                )[0]
                similarities[field].append(score)
        return similarities
