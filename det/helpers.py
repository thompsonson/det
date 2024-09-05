"""
Helpers Module

# helpers.py

This module provides utility functions designed to dynamically import and instantiate classes
based on runtime parameters. It is particularly useful for applications requiring flexibility
in loading different client or adapter classes without hardcoding their references.

The functions within facilitate the integration of various large language models (LLMs) and
embedding generators by constructing module paths and class names dynamically, then importing
and instantiating the corresponding classes.

Example usage:

    from helpers import get_llm_client, get_embedding_generator_adapter

    # Dynamically obtain and instantiate a client for a specific LLM provider and model
    llm_client = get_llm_client(llm_provider="GPT", llm_model="gpt-3")

    # Dynamically obtain and instantiate an embedding generator adapter
    embedding_generator = get_embedding_generator_adapter(
        embeddings_provider="OpenAI", embeddings_model="text-embedding-ada-002"
    )

Functions:
    - _get_client_class: A private function that imports and returns a class given its module path
         and name.
    - get_llm_client: Dynamically imports and instantiates a client class for interacting with a
        specified LLM provider and model.
    - get_embedding_generator_adapter: Dynamically imports and instantiates an adapter class for
        generating text embeddings with a specified provider and model.

The module supports extensibility by allowing new LLM providers and embedding generators to be
added to the system without modifying existing client code. It leverages Python's dynamic importing
capabilities to adapt to changes in available models or providers, ensuring the application can
evolve alongside the external services it interacts with.

"""

import importlib


def _get_client_class(module_path: str, class_name: str):
    """
    Dynamically imports and returns the specified client class.

    :param module_path: The module path where the class can be found.
    :param class_name: The name of the class to be imported.
    :return: The imported class.
    """
    module = importlib.import_module(module_path)
    return getattr(module, class_name)


def get_llm_client(llm_provider: str, llm_model: str, api_key: str = None):
    if not llm_provider:
        raise ValueError(f"Could not import class for {llm_provider}")
    if not llm_model:
        raise ValueError(f"Model is not given: {llm_model}")

    module_path = f"det.llm.llm_{llm_provider.lower()}"
    class_name = f"{llm_provider}Client"

    try:
        # Dynamically import the client class from the constructed module path
        ClientClass = _get_client_class(module_path, class_name)
        # Instantiate the client class, assuming a constructor that takes a model parameter
        if api_key:
            return ClientClass(model=llm_model, api_key=api_key)
        else:
            return ClientClass(model=llm_model)
    except ImportError as e:
        # Handle cases where the module or class does not exist
        raise ImportError(f"Could not import {class_name} from {module_path}: {e}")


def get_embedding_generator_adapter(embeddings_provider: str, embeddings_model: str):
    class_name = f"{embeddings_provider}EmbeddingGeneratorAdapter"
    module_path = "det.embeddings.adapters"

    try:
        # Use the dynamic module path and class name to get the class
        EmbeddingGeneratorClass = _get_client_class(module_path, class_name)
        # Instantiate the embedding generator class with the model name
        return EmbeddingGeneratorClass(model=embeddings_model)
    except ImportError as e:
        # Handle cases where the module or class does not exist
        raise ImportError(f"Could not import {class_name} from {module_path}: {e}")


def dynamic_import(class_path, init_obj=None):
    """Dynamically imports a class and optionally initializes it.

    Args:
        class_path (str): The full path to the class (e.g., 'module.submodule.ClassName').
        init_obj (optional): An object to pass to the class constructor.

    Returns:
        The imported class, or an instance of it if init_obj is provided.
    """
    module_name, class_name = class_path.rsplit(".", 1)
    module = importlib.import_module(module_name)
    cls = getattr(module, class_name, None)
    if cls and init_obj is not None:
        return cls(pydantic_object=init_obj)
    return cls
