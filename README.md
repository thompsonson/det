# LLM Response Analysis Framework

Welcome to a LLM Response Analysis Framework! This tool is designed to dive deep into the heart of Language Models (LLMs) and their intriguing responses. Designed for researchers, developers, and LLM enthusiasts, the framework offers a way to examine the consistency of Large Language Models and Agents build on them.

[Features](#features) | [Screenshots](#screenshots) | [Getting Started](#getting-started) | [Development](#development)

## Features

- **Dynamic LLM Integration**
Seamlessly connect with various LLM providers and models to fetch responses using a flexible architecture.

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

a basic analysis of OpenAI's gpt3.5-turbo model

`det --iterations 2 --llm-provider OpenAI --llm-model gpt-3.5-turbo --embeddings-provider OpenAI --embeddings-model text-embedding-ada-002`

## Development

### Documentation

The documentation is in the module headings. I'll probably move it out at some point but that's good for now :)

### Support and Contribution

For support, please open an issue on the GitHub repository. Contributions are welcome.

### License

This project is licensed under the MIT License - see the `LICENSE` file for details.
