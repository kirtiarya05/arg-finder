from collections import Counter

# ---------- FASTA READER ----------
def read_fasta(uploaded_file):
    if uploaded_file is None:
        return None

    content = uploaded_file.getvalue().decode("utf-8")
    lines = content.splitlines()

    sequence = ""
    for line in lines:
        if not line.startswith(">"):
            sequence += line.strip()

    return sequence.upper()


# ---------- SEQUENCE STATS ----------
def sequence_stats(seq):
    length = len(seq)
    counts = Counter(seq)

    gc = counts.get("G", 0) + counts.get("C", 0)
    gc_content = round((gc / length) * 100, 2) if length else 0

    return length, gc_content, counts


# ---------- ARG DATABASE ----------
ARG_DB = {
    "blaTEM": "ATGAGTATTCAACATTTCCG",
    "vanA": "ATGAATAGAATAAAAGTTGC",
    "tetM": "ATGAAAAAAATTCTTAAAGG",
}


def detect_genes(seq):
    found = []
    for gene, motif in ARG_DB.items():
        if motif in seq:
            found.append(gene)
    return found


# ---------- ORF DETECTION ----------
def find_orfs(seq):
    start = "ATG"
    stops = ["TAA", "TAG", "TGA"]

    orfs = []
    for i in range(len(seq)):
        if seq[i:i+3] == start:
            for j in range(i+3, len(seq), 3):
                if seq[j:j+3] in stops:
                    orfs.append(seq[i:j+3])
                    break
    return orfs


# ---------- RESISTANCE SCORE ----------
def resistance_score(gc, genes, orfs):
    score = gc + (len(genes) * 20) + (len(orfs) * 5)
    return round(score, 2)
