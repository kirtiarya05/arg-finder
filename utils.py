from Bio.Seq import Seq
from Bio import SeqIO
import io

def read_fasta(uploaded_file):
    stringio = io.StringIO(uploaded_file.getvalue().decode("utf-8"))
    record = SeqIO.read(stringio, "fasta")
    return str(record.seq)

def gc_content(sequence):
    g = sequence.count("G")
    c = sequence.count("C")
    return round((g + c) / len(sequence) * 100, 2)

def find_orfs(sequence):
    seq = Seq(sequence)
    orfs = []
    for i in range(3):
        trans = seq[i:].translate()
        if "*" in str(trans):
            orfs.append(str(trans))

    return orfs
