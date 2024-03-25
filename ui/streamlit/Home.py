import streamlit as st
import rag_vector_only
import rag_vector_graph
from PIL import Image
from ui_utils import render_header_svg
from langchain.globals import set_llm_cache
from langchain.cache import InMemoryCache

set_llm_cache(InMemoryCache())

st.set_page_config(page_icon="images/logo-mark-fullcolor-RGB-transBG.svg", layout="wide")

render_header_svg("images/vg-top-header.svg", 350)

render_header_svg("images/bottom-header.svg", 200)


def rag_v(question):
    res = rag_vector_only.get_results(question)
    st.markdown(res['result'])


def rag_vg(question):
    res = rag_vector_graph.get_results(question)
    st.markdown(res['result'])


question = st.text_input("Ask a question on Northwind data", value="")

col1, col2 = st.columns(2)
with col1:
    st.markdown("### Vector Only approach")
    with st.expander("Retrieves documents. May not include full context:"):
        vec_only = Image.open('./images/vector-only.png')
        st.markdown("#### Relationships are ignored. So, lesser context")
        st.image(vec_only)
        v = Image.open('./images/vector-only1.png')
        st.markdown("#### Sample Doc Chunk")
        st.image(v)
with col2:
    st.markdown("### Vector + Graph approach (GraphRAG)")
    with st.expander("Retrieves documents, relationships, and connected entities. Has full context:"):
        schema = Image.open('./images/schema.png')
        st.markdown("#### Relationships make this context-rich")
        st.image(schema)
        vg = Image.open('./images/vector-graph.png')
        st.markdown("#### Sample Doc Chunk")
        st.image(vg)

if question:
    with col1:
        with st.spinner('Running RAG using Vectors ...'):
            rag_v(question)
            st.success('Done!')
    with col2:
        with st.spinner('Running RAG using Vectors & Graphs ...'):
            rag_vg(question)
            st.success('Done!')

st.markdown("---")

st.markdown("""
<style>
  table {
    width: 100%;
    border-collapse: collapse;
    border: none !important;
    font-family: "Source Sans Pro", sans-serif;
    color: rgba(49, 51, 63, 0.6);
    font-size: 0.9rem;
  }

  tr {
    border: none !important;
  }
  
  th {
    text-align: center;
    colspan: 3;
    border: none !important;
    color: #0F9D58;
  }
  
  th, td {
    padding: 2px;
    border: none !important;
  }
</style>

<table>
  <tr>
    <th colspan="3">Sample questions to try</th>
  </tr>
  <tr>
    <td>What are the most popular cheeses? What customers buy the most of these?</td>
    <td>What are the most popular cheeses? What else can you recommend to go with?</td>
  </tr>
  <tr>
    <td></td>
    <td>What customers are buying the most caffeinated beverages? Can you also list the beverages and the amount they are buying?</td>
  </tr>
  <tr>
    <td></td>
    <td></td>
  </tr>
</table>
""", unsafe_allow_html=True)
