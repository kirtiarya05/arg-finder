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
    if not seq:
        return None

    length = len(seq)
    counts = Counter(seq)

    gc = counts.get("G", 0) + counts.get("C", 0)
    gc_content = round((gc / length) * 100, 2)

    return length, gc_content, counts
