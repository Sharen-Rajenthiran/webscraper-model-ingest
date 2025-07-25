import faiss
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
import numpy as np
from uuid import uuid4
from .config import settings
from utilities.logging_config import logging
from .webscraper import get_product_names_all
import logging

LOG = logging.getLogger(__name__)

EMBEDDINGS_MODEL = settings.EMBEDDINGS_MODEL

def get_products_and_prepare_for_embeddings():
    try:
        get_products_data = get_product_names_all()
    except Exception as e:
        LOG.error("Error retrieving the products: {e}")
        return []
    
    if not get_products_data:
        return []
    
    for_processing = list(product_dict.get("product") for product_dict in get_products_data)
    LOG.info(f"Successfully retrieved products list for processing. Retrieved {len(for_processing)} products")
    return for_processing

def create_langchain_documents(docs):
    return list(
        Document(page_content=content, metadata={"source": "zus/collections/drinkware"})
        for content in docs
    )

class ModelIngest:
    def __init__(self) -> None:
        self.docs_raw = get_products_and_prepare_for_embeddings()
        self.documents = create_langchain_documents(self.docs_raw)
        self.embeddings = self.load_huggingface_embeddings()

    def load_huggingface_embeddings(self, model=EMBEDDINGS_MODEL):
        embeddings = HuggingFaceEmbeddings(model_name=model)  
        LOG.info("HuggingFace embeddings model successfully retrieved.")
        return embeddings
    
    def create_vector_embeddings(self, docs_to_embed):
        embeddings = self.load_huggingface_embeddings()
        LOG.info("Successfully retrieved docs list.")

        if not docs_to_embed:
            LOG.debug(f"doc_list {docs_to_embed}")
            return []
        
        vector_embeddings = embeddings.embed_documents(docs_to_embed)

        LOG.info("Successfully created vector embeddings.")
        return vector_embeddings
    
    def create_faiss_vector_store(self, user_query):
        embeddings = self.load_huggingface_embeddings()
        index = faiss.IndexFlatL2(len(embeddings.embed_query(user_query)))

        vector_store = FAISS(
            embedding_function=embeddings,
            index=index,
            docstore=InMemoryDocstore(),
            index_to_docstore_id={},
        )

        uuids = [str(uuid4()) for _ in range(len(self.documents))]

        LOG.info(f"Successfully added documents to vector store with {len(self.documents)} documents")

        vector_store.add_documents(documents=self.documents)

        return vector_store
    
    def parse_output(self, results):
        parsed_output = list()

        for doc in results:
            parsed_output.append(
                {
                    "product": doc.page_content,
                    "source": doc.metadata.get("source", "no source found")
                    
                }
            )
        
        LOG.info(f"Successfully parsed output with {len(parsed_output)} items")
        return parsed_output
    
    def perform_top_k_search(self, user_query, top_k):
        vector_store = self.create_faiss_vector_store(user_query=user_query)

        LOG.info("Performing search...")
        results = vector_store.similarity_search(
           user_query,
            k=top_k,
        )

        LOG.info(f"Search completed. Found {len(results)} documents")
        return self.parse_output(results)
    
model = ModelIngest()