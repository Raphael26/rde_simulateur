import openai
import numpy as np
import pandas as pd
from typing import List, Dict, Tuple, Union


class EmbeddingGenerator:
    def __init__(self, openai_client=None):
        self.openai_client = openai_client
        #self.sentence_transformer_model = SentenceTransformer("all-MiniLM-L6-v2")

    #def create_with_sentence_transformers(self, texts):
    #    """Generate embeddings using SentenceTransformer."""
    #    return self.sentence_transformer_model.encode(texts)

    def create_embeddings(self, texts, provider="openai", model=None):
        """
        Generate embeddings using the specified provider.

        Args:
            texts (list): The input texts to embed
            provider (str): Either "openai" or "cohere"
            model (str, optional): The model to use for embeddings. If not specified, 
                                the default model for the provider will be used.
            **kwargs: Additional arguments to pass to the specific embedding function

        Returns:
            numpy.ndarray: Array of embeddings

        Raises:
            ValueError: If an unsupported provider is specified
        """            
        if provider.lower() == "openai":
            return self.create_with_openai(texts, model)
        #elif provider.lower() == "sentence_transformers":
        #    return self.create_with_sentence_transformers(texts)
        else:
            raise ValueError(f"Unsupported provider: {provider}")
        
    def create_with_openai(self, texts, model="text-embedding-3-large"):
        """Generate embeddings using OpenAI's API."""
        if not self.openai_client:
            raise ValueError("OpenAI client not provided")

        response = self.openai_client.embeddings.create(
            input=texts,
            model=model
        )
        return np.array([embedding.embedding for embedding in response.data])