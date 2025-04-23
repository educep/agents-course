# Party Planning Agent with Retrieval

This project demonstrates a simple Retrieval-Augmented Generation (RAG) system using SmolaAgents and LangChain to create a party planning assistant.

## Overview

The system implements a party planning agent that can retrieve relevant ideas for a superhero-themed party at Wayne Manor. The agent uses BM25 retrieval to find matching party planning suggestions from a small knowledge base.

## Components

- **PartyPlanningRetrieverTool**: A custom tool that uses BM25Retriever to perform lexical matching on party planning documents.
- **Knowledge Base**: A simulated collection of party planning ideas covering themes, entertainment, catering, and decorations.
- **LLM Integration**: Uses DeepSeek's language model through LiteLLM to process queries and generate responses.

## Technical Details

### BM25 Retriever

The system uses BM25 (Best Matching 25), which is a lexical retrieval algorithm that:

1. Counts term frequency with diminishing returns
2. Normalizes for document length
3. Weights terms by inverse document frequency (rare terms score higher)

Unlike true semantic search, BM25 focuses on matching exact words and their variations rather than understanding meaning. This means it performs well for direct keyword matching but may miss conceptual relationships where different words express the same idea.

### Document Processing

Documents are split into smaller chunks using RecursiveCharacterTextSplitter to optimize retrieval effectiveness. The system retrieves the top 5 most relevant documents for each query.

## Usage Example

```python
response = agent.run(
    "Find ideas for a luxury superhero-themed party, including entertainment, catering, and decoration options."
)
print(response)
```

## Future Improvements

For true semantic search capabilities, consider replacing BM25Retriever with an embedding-based approach:
- Use vector embeddings with models like OpenAI's text-embedding-ada-002
- Implement vector stores like FAISS, Chroma, or Pinecone
- Consider hybrid retrieval combining lexical and semantic approaches
