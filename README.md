[![Setup Poetry, check formatting and style, and run the tests](https://github.com/thompsonson/det/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/thompsonson/det/actions/workflows/ci-cd.yml)

# LLM Response Analysis Framework

Welcome to a LLM Response Analysis Framework! This tool is designed to dive deep into the heart of Language Models (LLMs) and their intriguing responses. Designed for researchers, developers, and LLM enthusiasts, the framework offers a way to examine the consistency of Large Language Models and Agents build on them.

[Features](#features) | [Screenshots](#screenshots) | [Getting Started](#getting-started) | [Development](#development)

## Current Version

Rev: v0.0.0

## Features

- **Dynamic LLM Integration**
Seamlessly connect with various LLM providers and models to fetch responses using a flexible architecture.

- **LangChain Structured Output Chain Analysis**
Seamlessly connect with a LangChain Structured Output and check for the consistency of responses. [See this documentation for further information.](docs/check_chain/README.md)

- **Semantic Similarity Calculation**
Understand the nuanced differences between responses by calculating their semantic distances.

- **Diverse Response Analysis**
Group, count, and analyze responses to highlight both their uniqueness and redundancy.

- **Rich Presentation**
Utilize beautiful tables and text differences to present analysis results in an understandable and visually appealing manner.

## Screenshots

Below are some screenshots showcasing the framework in action:

### GPT-3.5 Example

![GPT-3.5 Analysis](https://raw.githubusercontent.com/thompsonson/det/main/docs/img/GPT3.5.png)

### GPT-4 Example

![GPT-4 Analysis](https://raw.githubusercontent.com/thompsonson/det/main/docs/img/GPT4.png)


### LangChain Structure Output example (using gpt-4o)

![LangChain Structure Output example](https://raw.githubusercontent.com/thompsonson/det/main/docs/img/check_chain/results_for_gpt4o_20_iterations.png)


These visuals provide a glimpse into how the framework processes and presents data from different LLM versions, highlighting the flexibility and depth of analysis possible with this tool.

## Getting Started

### Prerequisites

- Ensure you have Python 3.10 or higher installed on your system.

### Installation

Install `det` using pip:

`pip install det`

### Configuration

Before using `det`, configure your LLM and embeddings provider API keys

`export OPENAI_API_KEY=sk-makeSureThisIsaRealKey`

### Basic Usage

To get a list of all the arguments and their descriptions, use:

`det --help`

a basic analysis of OpenAI's gpt-4o-mini model

```bash
det check-responses \
  --iterations 2 \
  --llm-provider OpenAI \
  --llm-model gpt-4o-mini \
  --embeddings-provider OpenAI \
  --embeddings-model text-embedding-ada-002
```

### LangChain Structured Output Chains

a LangChain Structured Output example

note, this requires the prompt details [/resources/prompt.json](/resources/prompts.json) and a pydantic output class [/resources/risk_definition.py](/resources/risk_definition.py)

```bash
det check-chain \
  --iterations 20 \
  --embeddings-provider OpenAI \
  --embeddings-model text-embedding-ada-002 \
  --prompt-config ./resources/prompts.json \
  --prompt-group RiskDefinition \
  --input-variables-str "risk_statement=There is a risk that failure to enforce multi-factor authentication can cause unauthorized access to user accounts to occur, leading to account takeover that could lead to financial fraud and identity theft issues for customers."
```

## Development

### Prerequisites
- [Python 3](https://www.python.org/downloads/)
- [Poetry](https://python-poetry.org/docs/#installation)

### Setup Instructions

1. Clone the repository:
   ```
   git clone https://github.com/thompsonson/det.git
   cd det
   ```

2. Set up the Poetry environment:
   ```
   poetry install
   ```

3. Activate the Poetry shell:
   ```
   poetry shell
   ```

You're now ready to start development on the `det` project!

### Documentation

The documentation is in the module headings. I'll probably move it out at some point but that's good for now :)

### Support and Contribution

For support, please open an issue on the GitHub repository. Contributions are welcome.

### License

This project is licensed under the MIT License - see the `LICENSE` file for details.
