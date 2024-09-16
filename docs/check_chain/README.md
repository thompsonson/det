# `det check-chain` Command Documentation

The `check-chain` command is part of the `det` project, which uses LangChain to perform structured output generation. This document provides a detailed explanation of the command, its usage, and interpretation of results, and the required resources.

## Command Structure

```bash
det check-chain \
  --iterations <num> \
  --embeddings-provider <provider> \
  --embeddings-model <model> \
  --prompt-config <path> \
  --prompt-group <group> \
  --input-variables-str <input>
```

### Parameters

- `--iterations`: Number of iterations to run (e.g., 20, 30)
- `--embeddings-provider`: Provider for embeddings (e.g., OpenAI)
- `--embeddings-model`: Specific model for embeddings (e.g., text-embedding-ada-002)
- `--prompt-config`: Path to the prompts configuration file (e.g., ./resources/prompts.json)
- `--prompt-group`: Group of prompts to use (e.g., RiskDefinition)
- `--input-variables-str`: Input variables as a string (e.g., "risk_statement=...")

## Example Usage

```bash
det check-chain \
  --iterations 20 \
  --embeddings-provider OpenAI \
  --embeddings-model text-embedding-ada-002 \
  --prompt-config ./resources/prompts.json \
  --prompt-group RiskDefinition \
  --input-variables-str "risk_statement=There is a risk that failure to enforce multi-factor authentication can cause unauthorized access to user accounts to occur, leading to account takeover that could lead to financial fraud and identity theft issues for customers."
```

## Output Interpretation

The command produces several outputs:

1. **Progress Bar**: Shows the progress of iterations.

   ![Progress Bar](docs/img/check_chain/command-to-run-checks.png)

2. **Structured Output**: The first response is a structured output based on the input risk statement. It includes fields such as:
   - risk_statement
   - risk_description
   - context
   - risk_categorization
   - security_controls
   - implementation_guidance
   - assessment_approach
   - risk_likelihood
   - risk_impact
   - authorization_recommendation
   - continuous_monitoring_strategy

   ![Structured Output](docs/img/check_chain/first_response_for_gpt4o_20_iterations.png)

3. **Semantic Similarity Scores**: Tables showing semantic similarity scores for each field across iterations.

   ![Semantic Similarity Scores](docs/img/check_chain/results_for_gpt4o_20_iterations.png)

   - Scores range from 0 to 1, where 1 indicates perfect similarity.
   - Higher scores suggest more consistent outputs across iterations.
   - Lower scores may indicate areas of variability or uncertainty in the model's responses.

## Interpretation Guidelines

- **High Consistency**: Fields with consistently high scores (close to 1.00) across iterations indicate stable and reliable outputs.
- **Variable Consistency**: Fields with more varied scores may require additional review or refinement in the prompt or model.
- **Low Scores**: Consistently low scores might suggest that the field is highly context-dependent or that the model struggles to provide consistent information for that aspect.

## Required Resources

The `check-chain` command relies on two key resource files, prompts.json and the definition of the Structured Output class.

Below discusses the ones used in the example and available in this repo. See [this cusomization documentation](Cusomtisation.md) for information on creating your own.

### 1. `prompts.json`

This file contains the configuration for the prompts used in the chain. Here's a breakdown of its structure:

```json
{
    "RiskDefinition": {
        "system_prompt": "...",
        "prompt": "...",
        "model": {
            "provider": "ChatOpenAI",
            "model": "gpt-4o",
            "max_tokens": "1500",
            "temperature": "0"
        },
        "outputparser": {
            "type": "langchain.output_parsers.PydanticOutputParser",
            "value": "resources.risk_definition.RiskDefinition"
        }
    }
}
```

- `system_prompt`: Provides context and instructions for the AI model.
- `prompt`: The specific prompt template used for generating responses.
- `model`: Specifies the AI model configuration.
- `outputparser`: Defines how the output should be parsed and structured.

### 2. `risk_definition.py`

This file contains the Pydantic model used for structuring the output. It defines the `RiskDefinition` class with the following fields:

- `risk_statement`: The original risk statement provided for analysis.
- `risk_description`: A detailed description of the risk aligned with NIST RMF terminology.
- `context`: Relevant background information and identification of critical assets involved.
- `risk_categorization`: Classification of the risk based on NIST SP 800-60 guidelines.
- `security_controls`: List of relevant NIST SP 800-53 controls associated with mitigating the risk.
- `implementation_guidance`: High-level suggestions for control implementation.
- `assessment_approach`: Methods to evaluate control effectiveness.
- `risk_likelihood`: Qualitative rating of the likelihood of the risk occurring.
- `risk_impact`: Qualitative rating of the impact of the risk, should it occur.
- `authorization_recommendation`: Recommendation for risk treatment strategy.
- `continuous_monitoring_strategy`: Proposed ongoing risk management activities.

Each field is defined with a description and, where applicable, constraints on the possible values (e.g., using `Literal` for fixed-choice fields).


## Note on Iterations

Running multiple iterations helps in assessing the consistency and reliability of the model's outputs. It's particularly useful for identifying which aspects of the risk assessment are most stable across multiple generations.


## How It Works

1. The `check-chain` command uses the `prompts.json` file to configure the LangChain prompt and model settings.
2. It then uses the `RiskDefinition` class from `risk_definition.py` to structure and validate the output from the language model.
3. The command runs for the specified number of iterations, generating structured risk definitions based on the input risk statement.
4. Finally, it calculates semantic similarity scores to assess the consistency of the generated outputs across iterations.
