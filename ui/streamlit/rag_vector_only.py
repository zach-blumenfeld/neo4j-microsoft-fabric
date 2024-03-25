from langchain.prompts.prompt import PromptTemplate
from langchain.llms.bedrock import Bedrock
from retry import retry
from timeit import default_timer as timer
import streamlit as st
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from neo4j_driver import run_query
from json import loads, dumps


PROMPT_TEMPLATE = """Human: You are a product and retail expert who can answer questions based only on the context below.
* Answer the question STRICTLY based on the context provided in JSON below.
* Do not assume or retrieve any information outside of the context 
* Think step by step before answering.
* Do not return helpful or extra text or apologies
* List the results in rich text format if there are more than one results

<question>
{input}
</question>

Here is the context:
<context>
{context}
</context>

Assistant:"""
PROMPT = PromptTemplate(
    input_variables=["input", "context"], template=PROMPT_TEMPLATE
)

EMBEDDING_MODEL = OpenAIEmbeddings(model="text-embedding-ada-002")


def vector_only_qa(query):
    query_vector = EMBEDDING_MODEL.embed_query(query)
    return run_query("""
    CALL db.index.vector.queryNodes('product_text_embeddings', 5, $queryVector)
    YIELD node AS doc, score
    RETURN doc.text as text, avg(score) AS score
    ORDER BY score DESC LIMIT 50
    """, params={'queryVector': query_vector})


def df_to_context(df):
    result = df.to_json(orient="records")
    parsed = loads(result)
    return dumps(parsed)


@retry(tries=5, delay=5)
def get_results(question):
    start = timer()
    try:
        llm = ChatOpenAI(temperature=0, model_name='gpt-4', streaming=True)
        df = vector_only_qa(question)
        ctx = df_to_context(df)
        ans = PROMPT.format(input=question, context=ctx)
        result = llm.invoke(ans)
        r = {'context': ans, 'result': result.content}
        return r
    finally:
        print('Cypher Generation Time : {}'.format(timer() - start))
