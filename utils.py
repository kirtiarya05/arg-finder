from Bio import SeqIO
import io

# -------- READ FASTA --------
def read_fasta(uploaded_file):
    stringio = io.StringIO(uploaded_file.getvalue().decode("utf-8"))
    record = SeqIO.read(stringio, "fasta")
    return str(record.seq)

# -------- GC CONTENT --------
def gc_content(seq):
    g = seq.count("G")
    c = seq.count("C")
    return round((g + c) / len(seq) * 100, 2)

# -------- FIND ORFs --------
def find_orfs(seq):
    start = "ATG"
    stop_codons = ["TAA", "TAG", "TGA"]
    orfs = []

    for i in range(len(seq) - 3):
        codon = seq[i:i+3]
        if codon == start:
            for j in range(i+3, len(seq)-3, 3):
                stop = seq[j:j+3]
                if stop in stop_codons:
                    orfs.append(seq[i:j+3])
                    break
    return orfs

# -------- DETECT GENES --------
def detect_genes(seq, db):
    matches = []
    for gene in db["gene"]:
        if gene in seq:
            matches.append(gene)
    return matches
