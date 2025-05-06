import chromadb
from llama_index.core import (
    PromptTemplate,
    Settings,
    SimpleDirectoryReader,
    StorageContext,
    VectorStoreIndex
)
from llama_index.core.node_parser import SentenceSplitter
from llama_index.llms.ollama import Ollama
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
import os
 
persist_dir = "./chroma_db" 
collection_name = "icp_brasil_docs" 
data_directory = "./data/" 
 
llm = Ollama(model="gemma3:12b")
embed_model = HuggingFaceEmbedding(model_name="intfloat/multilingual-e5-large")
 
Settings.llm = llm
Settings.embed_model = embed_model
 
if not os.path.exists(persist_dir):
    print(f"Diretório de persistência '{persist_dir}' não encontrado.")
    print(f"Criando novo índice a partir dos documentos em '{data_directory}'...")
 
    if not os.path.isdir(data_directory):
        print(f"Erro: O diretório de dados '{data_directory}' não foi encontrado.")
        exit()
 
    print(f"Carregando documentos PDF do diretório: {data_directory}")
    documents = SimpleDirectoryReader(
        input_dir=data_directory,
        required_exts=[".pdf"],
    ).load_data()
 
    if not documents:
        print(f"Nenhum documento PDF encontrado em '{data_directory}'.")
        exit()
    else:
        print(f"{len(documents)} documento(s) carregado(s) com sucesso.")
 
    print(f"Configurando ChromaDB persistente em '{persist_dir}'...")
    chroma_client = chromadb.PersistentClient(path=persist_dir)
    chroma_collection = chroma_client.get_or_create_collection(collection_name)
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
 
    print("Criando índice vetorial (pode levar tempo)...")
    index = VectorStoreIndex.from_documents(
        documents,
        storage_context=storage_context,
        embed_model=embed_model,
        transformations=[SentenceSplitter(chunk_size=800, chunk_overlap=120)], # Exemplo com chunk maior
        show_progress=True
    )
    
    print(f"Índice criado e salvo em '{persist_dir}'.")
 
else:
    print(f"Carregando índice existente do diretório: '{persist_dir}'...")
 
    chroma_client = chromadb.PersistentClient(path=persist_dir)
    try:
        chroma_collection = chroma_client.get_collection(collection_name)
    except Exception as e: 
         print(f"Erro ao carregar coleção '{collection_name}' de '{persist_dir}': {e}")
         print("Verifique se o diretório não está corrompido ou tente recriar o índice apagando a pasta.")
         exit()
 
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
 
    
    index = VectorStoreIndex.from_vector_store(
        vector_store=vector_store,
        embed_model=embed_model,
    )
    print("Índice carregado com sucesso.")
 
 
template = (
    """{context_str}
 
Você é um assistente jurídico especializado em certificação digital no âmbito do Instituto Nacional de Tecnologia da Informação (ITI) e da Infraestrutura de Chaves Públicas Brasileira (ICP-Brasil).
 
Seu papel é responder perguntas com base nos documentos fornecidos no contexto acima.

Pergunta: {query_str}
 
Resposta:"""
)
 
qa_template = PromptTemplate(template)
 
query_engine = index.as_query_engine(
    text_qa_template=qa_template,
    similarity_top_k=3
)
 
print("\nAssistente Jurídico ICP-Brasil (Persistente) - Pergunte algo ou digite 'sair' para encerrar.")
while True:
    user_input = input("\n Pergunta: ")
    if user_input.lower() in ["sair", "exit", "quit"]:
        print("Encerrando. Até mais!")
        break
 
    print("\nProcessando sua pergunta...")
    response = query_engine.query(user_input)
    print("\nResposta:\n", response.response)
