from pinecone import (
    Pinecone,
    ServerlessSpec,
    PineconeApiException,
)


class PineconeManager:
    def __init__(self, api_key):
        """
        Initialize the Pinecone client with the provided API key and optional embedding clients.
        
        Args:
            api_key (str): Pinecone API key
        """
        self.client = Pinecone(api_key=api_key)

    def get_index(self, index_name):
        """
        Get a Pinecone index by name.
        
        Args:
            index_name (str): Name of the index to retrieve
            
        Returns:
            pinecone.Index: The index object
        """
        return self.client.Index(index_name)

    def get_all_indexes(self):
        """
        Get the list of indexes available in the Pinecone account.
        """
        all_indexes = self.client.list_indexes()
        return [index_info["name"] for index_info in all_indexes]

    def delete_index(self, index_name):
        """Delete an index."""
        # Get the list of indexes
        indexes = self.get_all_indexes()

        # Safely delete the index if it already exists
        if index_name in indexes:
            try:
                self.client.delete_index(index_name)
                print(f"Index deleted {index_name} successfully.")
            except Exception as e:
                print(f"Warning: Failed to delete index: {e}.")    
    
    def create_index(self, index_name, dimension, delete=False):
        """
        Create a Pinecone index with the specified parameters.
        
        Args:
            index_name (str): Name of the index to create
            dimension (int): Dimension of the vectors
            delete (bool): Whether to delete the index if it already exists
            
        Returns:
            pinecone.Index: The created index
        """
        # Delete index first if needed
        if delete:
            self.delete_index(index_name)
        
        # Create the index
        try:
            self.client.create_index(
                name=index_name,
                vector_type="dense",
                dimension=dimension,
                metric="cosine",
                spec=ServerlessSpec(
                    cloud="aws",
                    region="us-east-1"
                ),
                deletion_protection="disabled",
                tags={
                    "environment": "development"
                }
            )
            print("Index created successfully.")
            return self.client.Index(index_name)
        
        except PineconeApiException as e:
            if "ALREADY_EXISTS" in e.body:
                print("The index already exists, choose another name or delete first.")

    def upsert_entries(self, entries, index, namespace):
        """
        Upsert entries to a Pinecone index in batches.
        
        Args:
            entries (list): List of entries to upsert in the index
            index: Pinecone Index object or index name string
            namespace (str): Namespace to upsert vectors into
        """
        # Handle both index object and index name
        if isinstance(index, str):
            index = self.client.Index(index)
    
        # Define batch size
        batch_size=100
    
        # Upsert in batches
        for i in range(0, len(entries), batch_size):
            batch = entries[i:i+batch_size]
            try:
                index.upsert(
                    vectors=batch,
                    namespace=namespace
                )
            except Exception as e:
                print(f"Error upserting batch: {e}.")