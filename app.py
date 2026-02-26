import streamlit as st
import plotly.express as px
from utils import read_fasta, sequence_stats, nucleotide_dataframe

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="ARG Finder",
    page_icon="🧬",
    layout="wide"
)

# ---------- CUSTOM CSS ----------
st.markdown("""
<style>
.block-container {
    padding-top: 2rem;
}
.metric-card {
    background: #111827;
    padding: 20px;
    border-radius: 14px;
    text-align: center;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# ---------- HEADER ----------
st.title("🧬 ARG Finder Dashboard")
st.caption("Upload FASTA → Analyze sequence → Visual insights")

# ---------- FILE UPLOAD ----------
uploaded = st.file_uploader(
    "Upload FASTA file",
    type=["fasta", "fa", "txt"]
)

if uploaded is None:
    st.info("Upload a FASTA file to begin analysis")
    st.stop()

# ---------- PROCESS ----------
with st.spinner("Reading sequence..."):
    sequence = read_fasta(uploaded)

if not sequence:
    st.error("Invalid FASTA file")
    st.stop()

stats = sequence_stats(sequence)

# ---------- METRICS ----------
col1, col2, col3 = st.columns(3)

col1.metric("Sequence Length", stats["length"])
col2.metric("GC Content %", stats["gc_content"])
col3.metric("Unique Bases", len(stats["counts"]))

# ---------- SEQUENCE PREVIEW ----------
with st.expander("Sequence Preview"):
    st.text_area("", sequence[:2000], height=200)

# ---------- VISUALIZATION ----------
df = nucleotide_dataframe(stats["counts"])

col4, col5 = st.columns(2)

# Bar chart
fig_bar = px.bar(
    df,
    x="Nucleotide",
    y="Count",
    title="Nucleotide Distribution",
    text="Count"
)

col4.plotly_chart(fig_bar, use_container_width=True)

# Pie chart
fig_pie = px.pie(
    df,
    names="Nucleotide",
    values="Count",
    title="Composition"
)

col5.plotly_chart(fig_pie, use_container_width=True)

# ---------- GC GAUGE ----------
fig_gauge = px.bar(
    x=["GC Content"],
    y=[stats["gc_content"]],
    text=[f'{stats["gc_content"]}%'],
    title="GC Content Overview"
)

st.plotly_chart(fig_gauge, use_container_width=True)

# ---------- DOWNLOAD ----------
st.download_button(
    "Download Sequence",
    sequence,
    file_name="sequence.txt"
)
