# Standard imports
import asyncio

# Third party imports
from llama_index.core import SimpleDirectoryReader
from llama_index.core.ingestion import IngestionPipeline
from llama_index.core.node_parser import SentenceSplitter
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

# Internal imports
from src.llamaindex_ag.b1_load_local_sets import load_local_sets, this_path

# ---------  Cargamos y embeddamos los documentos de las personas ---------
load_local_sets()
reader = SimpleDirectoryReader(input_dir=this_path)
documents = reader.load_data()
len(documents)

# create the pipeline with transformations
embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
pipeline = IngestionPipeline(transformations=[SentenceSplitter(), embed_model])


async def process_documents():
    """Process documents asynchronously."""
    # run the pipeline async
    nodes = await pipeline.arun(documents=documents[:10])
    return nodes


nodes = asyncio.run(process_documents())
