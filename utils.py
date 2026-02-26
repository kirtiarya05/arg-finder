import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from utils import read_fasta, gc_content, find_orfs, detect_genes

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="ARG Finder",
    page_icon="🧬",
    layout="centered"
)

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.header("🧬 About This Project")
    st.write(
        "ARG Finder is a bioinformatics tool that analyzes DNA sequences "
        "and predicts potential antibiotic resistance markers."
    )
    st.write("Built using:")
    st.write("- Streamlit")
    st.write("- Biopython")
    st.write("- Pandas")
    st.write("- Matplotlib")

# ---------------- MAIN HEADER ----------------
st.title("🧬 ARG Finder — Antibiotic Resistance Predictor")

st.markdown("""
Upload a **DNA FASTA file** and this tool will:

• Calculate GC content  
• Detect resistance genes  
• Estimate resistance score  
• Identify open reading frames (ORFs)  
""")

# ---------------- FILE UPLOAD ----------------
uploaded = st.file_uploader("📂 Upload FASTA file", type=["fasta", "fa"])

# ---------------- ANALYSIS ----------------
if uploaded:

    st.info("Analyzing sequence...")

    # Read DNA sequence
    sequence = read_fasta(uploaded)

    # Load resistance database
    db = pd.read_csv("resistance_db.csv")

    # Perform calculations
    gc = gc_content(sequence)
    orfs = find_orfs(sequence)
    matches = detect_genes(sequence, db)

    # Resistance score formula
    score = round(gc + len(matches) * 10, 2)

    # ---------------- RESULTS SECTION ----------------
    st.subheader("📊 Results")

    col1, col2 = st.columns(2)

    col1.metric("GC Content", f"{gc}%")
    col2.metric("ORFs Found", len(orfs))

    st.success(f"Resistance Score: {score}")

    # ---------------- GENE RESULTS ----------------
    st.subheader("🧬 Detected Resistance Genes")

    if matches:
        st.write(matches)
    else:
        st.warning("No resistance genes detected in this sequence.")

    # ---------------- VISUALIZATION ----------------
    st.subheader("📈 Visualization")

    # ORF Length Graph (Always visible if ORFs exist)
    if orfs:
        lengths = [len(o) for o in orfs]

        fig1, ax1 = plt.subplots()
        ax1.plot(lengths, marker="o")
        ax1.set_title("ORF Length Distribution")
        ax1.set_xlabel("ORF Index")
        ax1.set_ylabel("Length (bp)")

        st.pyplot(fig1)

    else:
        st.info("No ORFs found to visualize.")

    # Gene Bar Chart (Only if genes detected)
    if matches:
        gene_counts = {gene: 1 for gene in matches}

        fig2, ax2 = plt.subplots()
        ax2.bar(gene_counts.keys(), gene_counts.values())
        ax2.set_title("Detected Resistance Genes")
        ax2.set_ylabel("Presence")

        st.pyplot(fig2)

    st.balloons()

else:
    st.warning("Please upload a FASTA file to begin analysis.")
