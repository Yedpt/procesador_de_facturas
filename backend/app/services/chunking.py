from langchain_text_splitters import RecursiveCharacterTextSplitter

def split_text_into_chunks(text:str, chunk_size:int = 800, chunk_overlap:int = 100) -> list[dict]:
    """
    Divide el texto en fragmentos utilizando RecursiveCharacterTextSplitter de LangChain.
    """

    splitter = RecursiveCharacterTextSplitter(
        chunk_size= chunk_size,
        chunk_overlap= chunk_overlap,
    )

    docs = splitter.create_documents([text])

    chunks = []

    for i, doc in enumerate(docs):
        chunks.append({
            "chunk_id": f"chunk_{i+1}",
            "content": doc.page_content,
            "start_index": doc.metadata.get("start_index"),
        })

    return chunks