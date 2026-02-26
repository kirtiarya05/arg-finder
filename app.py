import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from utils import read_fasta, sequence_stats

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="ARG Finder",
    page_icon="🧬",
    layout="wide"
)

# ---------- HEADER ----------
st.title("🧬 ARG Finder — DNA Sequence Analyzer")
st.markdown("""
Upload a FASTA file to analyze:
- Sequence length
- GC content
- Nucleotide distribution
""")

# ---------- FILE UPLOAD ----------
uploaded = st.file_uploader(
    "Upload FASTA file",
    type=["fasta", "fa", "txt"]
)

if uploaded is None:
    st.info("Please upload a FASTA file to begin.")
    st.stop()

# ---------- PROCESS ----------
sequence = read_fasta(uploaded)

if not sequence:
    st.error("Invalid FASTA file.")
    st.stop()

length, gc_content, counts = sequence_stats(sequence)

# ---------- METRICS ----------
col1, col2, col3 = st.columns(3)

col1.metric("Sequence Length", length)
col2.metric("GC Content (%)", gc_content)
col3.metric("Unique Bases", len(counts))

# ---------- SEQUENCE PREVIEW ----------
with st.expander("Preview Sequence"):
    st.text_area("", sequence[:2000], height=200)

# ---------- VISUALIZATION ----------
st.subheader("📊 Nucleotide Distribution")

df = pd.DataFrame({
    "Nucleotide": list(counts.keys()),
    "Count": list(counts.values())
})

fig, ax = plt.subplots()
ax.bar(df["Nucleotide"], df["Count"])
ax.set_xlabel("Nucleotide")
ax.set_ylabel("Count")
ax.set_title("Nucleotide Frequency")

st.pyplot(fig)

# ---------- GC VISUAL ----------
st.subheader("🧪 GC Content Overview")

fig2, ax2 = plt.subplots()
ax2.bar(["GC Content"], [gc_content])
ax2.set_ylim(0, 100)
ax2.set_ylabel("Percentage")
ax2.set_title("GC Content Percentage")

st.pyplot(fig2)

# ---------- FOOTER ----------
st.success("Analysis Complete ✅")
