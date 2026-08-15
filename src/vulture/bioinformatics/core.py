"""Bioinformatics: FASTA/FASTQ minimal parsers.
"""

def parse_fasta(stream):
    name = None
    seq = []
    for line in stream:
        line = line.strip()
        if not line:
            continue
        if line.startswith('>'):
            if name:
                yield name, ''.join(seq)
            name = line[1:]
            seq = []
        else:
            seq.append(line)
    if name:
        yield name, ''.join(seq)
