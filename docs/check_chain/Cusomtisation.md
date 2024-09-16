# `det check-chain` Command Documentation - Cusomization

## Customizing Resources for Different Use Cases

While the provided example focuses on risk assessment, the `check-chain` command can be adapted for various use cases such as sentiment analysis, text summarization, or any other structured output generation task. Here's how you can customize the resources for your specific use case:

### 1. Modifying `prompts.json`

1. Create a new key in the JSON object for your use case (e.g., "SentimentAnalysis" or "TextSummarization").
2. Adjust the `system_prompt` to provide context and instructions relevant to your task.
3. Update the `prompt` to include the appropriate input variables and instructions for your use case.
4. Modify the `model` settings if needed (e.g., changing the model or adjusting parameters).
5. Update the `outputparser` to point to your custom Pydantic model.

Example for sentiment analysis:

```json
{
    "SentimentAnalysis": {
        "system_prompt": "You are a sentiment analysis expert. Your task is to analyze the sentiment of given text and provide a detailed breakdown.",
        "prompt": "Analyze the sentiment of the following text:\n\n{input_text}\n\nProvide a detailed analysis as specified in the format instructions.",
        "model": {
            "provider": "ChatOpenAI",
            "model": "gpt-4",
            "max_tokens": "500",
            "temperature": "0.2"
        },
        "outputparser": {
            "type": "langchain.output_parsers.PydanticOutputParser",
            "value": "resources.sentiment_analysis.SentimentAnalysis"
        }
    }
}
```

### 2. Creating a Custom Pydantic Model

1. Create a new Python file (e.g., `sentiment_analysis.py`) in the resources directory.
2. Define a new Pydantic model with fields relevant to your use case.

Example for sentiment analysis:

```python
from langchain_core.pydantic_v1 import BaseModel, Field
from typing import List, Literal

class SentimentAnalysis(BaseModel):
    input_text: str = Field(..., description="The original text provided for analysis.")
    overall_sentiment: Literal["Very Negative", "Negative", "Neutral", "Positive", "Very Positive"] = Field(..., description="The overall sentiment of the text.")
    sentiment_score: float = Field(..., ge=-1, le=1, description="Sentiment score from -1 (very negative) to 1 (very positive).")
    key_phrases: List[str] = Field(..., description="List of key phrases that contribute to the sentiment.")
    explanation: str = Field(..., description="Detailed explanation of the sentiment analysis.")
```

### 3. Updating the Command

When using your custom resources, update the `check-chain` command accordingly:

```bash
det check-chain --iterations 20 --embeddings-provider OpenAI --embeddings-model text-embedding-ada-002 --prompt-config ./resources/prompts.json --prompt-group SentimentAnalysis --input-variables-str "input_text=Your text for sentiment analysis goes here."
```

### Tips for Customization

1. Ensure that your Pydantic model fields align with the output you expect from the language model.
2. Adjust the system prompt and main prompt to guide the model towards producing the desired structured output.
3. Consider the appropriate model and parameters for your use case (e.g., you might need fewer tokens for sentiment analysis compared to risk assessment).
4. Test your custom setup with various inputs to ensure it produces consistent and accurate results.
5. You may need to adjust the semantic similarity analysis based on the fields in your custom model.

By following these steps, you can adapt the `check-chain` command for a wide range of use cases while maintaining the benefits of structured output and consistency analysis.
