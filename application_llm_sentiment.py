from langchain_openai import ChatOpenAI
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain_core.prompts import ChatPromptTemplate
from application_loader_embedder import load_embed
from application_text_to_json import text_to_json


def sentimental_analysis_llm(url):
    """
    1. use this to pick either llama 3 or openAI LLM
    """
    # llm = Ollama(model="llama3")
    llm = ChatOpenAI(
        model="gpt-4o",
        temperature=0.3
    )

    """
    2. load function to embedded and vector base
    """
    vector = load_embed(url)

    if vector is None:
        return None
    else:
        """
        3. construct a chain template
        """
        prompt = ChatPromptTemplate.from_template("""
        Answer the following question based only on the provided context:
        
        <context>
        {context}
        </context>
        
        Question: {input}""")

        document_chain = create_stuff_documents_chain(llm, prompt)
        retriever = vector.as_retriever()
        retrieval_chain = create_retrieval_chain(retriever, document_chain)

        # 4. run/invoke the chain to get
        response = retrieval_chain.invoke(
            {"input": "What stocks are mentioned, and give me sentimental level for each stock, "
                      "from bearish to "
                      "neutral to bullish. If not available, add NA. Add one sentence for context on each sentimental. "
                      "Give me the answer in JSON format "})
        print(response["answer"])
        # response_json = text_to_json(response["answer"])
        return response["answer"]

"""
Test the function
"""
# result = sentimental_analysis_llm("https://www.fool.com/investing/2024/06/01/should-you-buy-nvidia-stock-before-june-6/")
# result = sentimental_analysis_llm("https://www.benzinga.com/news/24/06/39213518/chip-etfs-in-focus-on-new-generation-ai-product-launches")
# if result is None:
#     print("no answer found")
# else:
#     print(result)