import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from utils import read_fasta, sequence_stats, detect_genes, find_orfs, resistance_score

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="ARG Finder", page_icon="🧬", layout="wide")

st.title("🧬 ARG Finder — Antibiotic Resistance Predictor")

st.markdown("""
Upload a FASTA file to:
- Calculate GC content
- Detect resistance genes
- Identify ORFs
- Estimate resistance score
""")

# ---------- UPLOAD ----------
uploaded = st.file_uploader("Upload FASTA file", type=["fasta", "fa", "txt"])

if not uploaded:
    st.info("Upload a FASTA file to begin.")
    st.stop()

sequence = read_fasta(uploaded)

if not sequence:
    st.error("Invalid FASTA file.")
    st.stop()

# ---------- ANALYSIS ----------
length, gc_content, counts = sequence_stats(sequence)
genes = detect_genes(sequence)
orfs = find_orfs(sequence)
score = resistance_score(gc_content, genes, orfs)

# ---------- METRICS ----------
c1, c2, c3, c4 = st.columns(4)
c1.metric("Length", length)
c2.metric("GC %", gc_content)
c3.metric("Genes", len(genes))
c4.metric("ORFs", len(orfs))

st.subheader(f"⚠ Resistance Score: {score}")

# ---------- NUCLEOTIDE PLOT ----------
st.subheader("📊 Nucleotide Distribution")

df = pd.DataFrame({
    "Nucleotide": list(counts.keys()),
    "Count": list(counts.values())
})

fig, ax = plt.subplots()
ax.bar(df["Nucleotide"], df["Count"])
ax.set_title("Nucleotide Frequency")
st.pyplot(fig)

# ---------- GC PLOT ----------
st.subheader("🧪 GC Content")

fig2, ax2 = plt.subplots()
ax2.bar(["GC"], [gc_content])
ax2.set_ylim(0, 100)
st.pyplot(fig2)

# ---------- GENES ----------
st.subheader("🧬 Detected ARG Genes")

if genes:
    st.success(", ".join(genes))
else:
    st.warning("No ARG genes detected")

# ---------- ORF VIEW ----------
st.subheader("🧪 ORF Preview")

if orfs:
    st.text(orfs[0][:200] + "...")
else:
    st.warning("No ORFs detected")

# ---------- DOWNLOAD REPORT ----------
report = {
    "Length": length,
    "GC Content": gc_content,
    "Genes": genes,
    "ORFs": len(orfs),
    "Resistance Score": score
}

report_df = pd.DataFrame([report])

st.download_button(
    "📥 Download Report CSV",
    report_df.to_csv(index=False),
    file_name="arg_report.csv"
)

st.success("Analysis Complete ✅")
