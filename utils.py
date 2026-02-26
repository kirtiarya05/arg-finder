from collections import Counter

# ---------- FASTA ----------
def read_fasta(uploaded_file):
    content = uploaded_file.getvalue().decode("utf-8")
    seq = ""
    for line in content.splitlines():
        if not line.startswith(">"):
            seq += line.strip()
    return seq.upper()


# ---------- STATS ----------
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


# ---------- BLAST-LIKE SEARCH ----------
def similarity_search(seq):
    results = {}
    for gene, motif in ARG_DB.items():
        score = seq.count(motif)
        results[gene] = score
    return results


# ---------- ORF ----------
def find_orfs(seq):
    start, stops = "ATG", ["TAA", "TAG", "TGA"]
    orfs = []
    for i in range(len(seq)):
        if seq[i:i+3] == start:
            for j in range(i+3, len(seq), 3):
                if seq[j:j+3] in stops:
                    orfs.append(seq[i:j+3])
                    break
    return orfs


# ---------- PROTEIN TRANSLATION ----------
CODON_TABLE = {
    "ATA":"I","ATC":"I","ATT":"I","ATG":"M",
    "ACA":"T","ACC":"T","ACG":"T","ACT":"T",
    "AAC":"N","AAT":"N","AAA":"K","AAG":"K",
    "AGC":"S","AGT":"S","AGA":"R","AGG":"R",
    "CTA":"L","CTC":"L","CTG":"L","CTT":"L",
    "CCA":"P","CCC":"P","CCG":"P","CCT":"P",
    "CAC":"H","CAT":"H","CAA":"Q","CAG":"Q",
    "CGA":"R","CGC":"R","CGG":"R","CGT":"R",
    "GTA":"V","GTC":"V","GTG":"V","GTT":"V",
    "GCA":"A","GCC":"A","GCG":"A","GCT":"A",
    "GAC":"D","GAT":"D","GAA":"E","GAG":"E",
    "GGA":"G","GGC":"G","GGG":"G","GGT":"G",
    "TCA":"S","TCC":"S","TCG":"S","TCT":"S",
    "TTC":"F","TTT":"F","TTA":"L","TTG":"L",
    "TAC":"Y","TAT":"Y","TAA":"_","TAG":"_",
    "TGC":"C","TGT":"C","TGA":"_","TGG":"W",
}

def translate(seq):
    protein = ""
    for i in range(0, len(seq)-2, 3):
        codon = seq[i:i+3]
        protein += CODON_TABLE.get(codon, "X")
    return protein


# ---------- MUTATION DETECTION ----------
def mutation_scan(seq):
    mutations = []
    for gene, motif in ARG_DB.items():
        if motif not in seq:
            if motif[:10] in seq:
                mutations.append(f"Partial mutation near {gene}")
    return mutations
