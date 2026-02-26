import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

from utils import *
from ml_model import predict_resistance

st.set_page_config(page_title="ARG Finder", page_icon="🧬", layout="wide")

# DARK THEME
st.markdown("""
<style>
body { background-color: #0e1117; color: white; }
</style>
""", unsafe_allow_html=True)

st.title("🧬 ARG Finder — AI Bioinformatics Platform")

uploaded = st.file_uploader("Upload FASTA", type=["fasta","fa","txt"])

if not uploaded:
    st.stop()

seq = read_fasta(uploaded)

length, gc, counts = sequence_stats(seq)
genes = detect_genes(seq)
orfs = find_orfs(seq)
blast = similarity_search(seq)
protein = translate(seq[:300])
mutations = mutation_scan(seq)
ml_pred = predict_resistance(gc, len(orfs), len(genes))

# ---------- METRICS ----------
c1,c2,c3,c4 = st.columns(4)
c1.metric("Length", length)
c2.metric("GC%", gc)
c3.metric("Genes", len(genes))
c4.metric("ORFs", len(orfs))

st.subheader(f"🤖 ML Prediction: {ml_pred}")

# ---------- PLOTS ----------
df = pd.DataFrame({"Nucleotide": list(counts.keys()), "Count": list(counts.values())})
fig, ax = plt.subplots()
ax.bar(df["Nucleotide"], df["Count"])
st.pyplot(fig)

# ---------- BLAST ----------
st.subheader("🔎 Similarity Search")
st.write(blast)

# ---------- PROTEIN ----------
st.subheader("🧬 Protein Translation Preview")
st.text(protein[:200])

# ---------- MUTATIONS ----------
st.subheader("⚠ Mutation Scan")
st.write(mutations if mutations else "No mutations")

# ---------- PDF REPORT ----------
def create_pdf():
    doc = SimpleDocTemplate("report.pdf")
    styles = getSampleStyleSheet()
    content = [
        Paragraph(f"GC: {gc}", styles["Normal"]),
        Paragraph(f"Genes: {genes}", styles["Normal"]),
        Paragraph(f"Prediction: {ml_pred}", styles["Normal"])
    ]
    doc.build(content)

create_pdf()

with open("report.pdf", "rb") as f:
    st.download_button("📄 Download PDF", f, "report.pdf")

st.success("Analysis complete")
