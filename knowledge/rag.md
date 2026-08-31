# RAG Knowledge Base

## Retrieval-Augmented Generation

RAG combines information retrieval with language generation.

Instead of relying only on the language model's internal knowledge, the system retrieves relevant information from an external knowledge base and provides it as context to the model.

## Document Processing

Documents are first processed and divided into smaller chunks.

Chunking allows relevant portions of large documents to be retrieved without providing the entire document to the language model.

## Embeddings

Embeddings represent text as numerical vectors.

Semantically similar pieces of text have similar vector representations.

## Vector Database

Embeddings can be stored in a vector database or vector index.

The system can perform similarity search to find chunks relevant to a query.

FAISS is an example of a library used for efficient similarity search over vectors.

## Retrieval

During retrieval, the user's query or another input is converted into an embedding.

The vector store is searched for the most relevant chunks.

## Generation

The retrieved chunks are provided to the language model as context.

The language model then generates an answer using the retrieved information.

## RAG Evaluation

A RAG system can be evaluated separately for retrieval quality and generation quality.

Retrieval should return relevant information, while generation should produce an accurate answer grounded in the retrieved context.