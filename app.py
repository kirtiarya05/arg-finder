import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from utils import read_fasta, gc_content, find_orfs, detect_genes

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="ARG Finder", page_icon="🧬", layout="centered")

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.header("🧬 About")
    st.write(
        "ARG Finder is a bioinformatics mini-tool that analyzes DNA sequences "
        "to detect antibiotic resistance genes and genomic features."
    )
    st.write("**Tech Stack:** Streamlit, Biopython, Pandas, Matplotlib")
    st.write("Created for learning bioinformatics + Python deployment.")

# ---------------- MAIN UI ----------------
st.title("🧬 ARG Finder — Antibiotic Resistance Predictor")
st.markdown(
    "Upload a **DNA FASTA file** and this tool will:\n"
    "- Calculate GC content\n"
    "- Detect resistance genes\n"
    "- Estimate resistance score\n"
    "- Identify open reading frames (ORFs)"
)

# ---------------- FILE UPLOAD ----------------
uploaded = st.file_uploader("📂 Upload FASTA file", type=["fasta", "fa"])

# ---------------- PROCESSING ----------------
if uploaded:
    st.info("Analyzing sequence...")

    # Read sequence
    sequence = read_fasta(uploaded)

    # Load resistance database
    db = pd.read_csv("resistance_db.csv")

    # Perform analysis
    gc = gc_content(sequence)
    matches = detect_genes(sequence, db)
    orfs = find_orfs(sequence)

    # Resistance score formula
    score = round(gc + len(matches) * 10, 2)

    # ---------------- RESULTS ----------------
    st.subheader("📊 Results")

    col1, col2 = st.columns(2)
    col1.metric("GC Content", f"{gc}%")
    col2.metric("ORFs Found", len(orfs))

    st.success(f"Resistance Score: {score}")

    st.write("### 🧬 Detected Genes")
    if matches:
        st.write(matches)
    else:
        st.warning("No resistance genes detected.")

    # ---------------- VISUALIZATION ----------------
    if matches:
        gene_counts = {gene: 1 for gene in matches}

        fig, ax = plt.subplots()
        ax.bar(gene_counts.keys(), gene_counts.values())
        ax.set_title("Detected Resistance Genes")
        ax.set_ylabel("Presence")

        st.pyplot(fig)

    st.balloons()

else:
    st.warning("Please upload a FASTA file to start analysis.")
