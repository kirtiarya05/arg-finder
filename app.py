st.set_page_config(page_title="ARG Finder", page_icon="🧬")
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from utils import read_fasta, gc_content, find_orfs
from model import resistance_score

#title
st.title("🧬 ARG Finder — Antibiotic Resistance Predictor")
st.info("Upload DNA FASTA file to detect resistance genes and genomic features.")

# Sidebar info
st.sidebar.title("About")
st.sidebar.info("This tool analyzes DNA sequences and predicts antibiotic resistance genes.")

# Upload FASTA file
uploaded = st.file_uploader("Upload FASTA file")

# Run analysis only if file uploaded
if uploaded:
    # Read sequence
    sequence = read_fasta(uploaded)

    st.write("Sequence Length:", len(sequence))

    # Load resistance database
    db = pd.read_csv("resistance_db.csv")

    # Motif search
    matches = []
    for _, row in db.iterrows():
        if row["motif"] in sequence:
            matches.append(row["gene"])

    # Biological metrics
    gc = gc_content(sequence)
    orfs = find_orfs(sequence)
    score = resistance_score(matches, gc)

    # Results
    st.subheader("Results")
    st.write("GC Content:", gc)
    st.write("Detected Genes:", matches)
    st.write("Resistance Score:", score)
    st.write("ORFs Found:", len(orfs))

    st.success(f"Resistance Score: {score}")

    # 📊 Bar chart for detected genes
    if matches:
        gene_counts = {gene: 1 for gene in matches}
        plt.figure()
        plt.bar(gene_counts.keys(), gene_counts.values())
        plt.title("Detected Resistance Genes")
        st.pyplot(plt)

    # 🧬 Pie chart for GC vs AT
    at = 100 - gc
    plt.figure()
    plt.pie([gc, at], labels=["GC", "AT"], autopct="%1.1f%%")
    plt.title("GC vs AT Composition")

    st.pyplot(plt)
