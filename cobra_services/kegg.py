import re
from Bio.KEGG import REST
from Bio.SeqUtils import molecular_weight


def ecnumber_to_genes(ECnumber):
    """
    Dictionary of organism => gene for a reaction.
    """
    # TODO: Make sure the genes addresses are stripped correctly.

    text = REST.kegg_get('ec:' + ECnumber).read()

    try:
        start_index = text.index('GENES') + 5
        end_index = text.index('DBLINKS')
    except ValueError:
        ec_index = text.find('Now EC ')
        if ec_index == -1:
            return {}
        else:
            new_ec = text[start_index+6: start_index+20].split(',')[0]
            return ecnumber_to_genes(new_ec)
    gene_list = text[start_index: end_index].split('\n')
    gene_list = [g.strip().split(': ') for g in gene_list]

    gene_dict = {}
    for entry in gene_list:
            split_seq = list(filter(None, re.split("[, \-:()]+", entry)))
            f_seq = []
            if split_seq == []:
                continue
            for entry in split_seq:
                f_seq.append(entry.strip())
            gene_dict[f_seq[0]] = list(filter(lambda x: x.isdigit(), f_seq))

    return gene_dict


def kegggene_to_sequence(organism, kegggene):
    """
    Get the sequence of a gene
    """

    text = REST.kegg_get(organism.lower() + ':' + kegggene).read()

    start_index = text.index('AASEQ')
    end_index = text.index('NTSEQ')

    raw_code = text[start_index: end_index].split('\n', 1)[1]
    code = raw_code.split('\n')
    sequence = ''
    for piece in code:
        sequence = sequence + piece.strip()

    return sequence


def sequence_weight(sequence):
    "Return weight in Daltons"
    ambigous_count = sequence.count('X')
    mod_seqeunce = sequence.replace('X', '')
    weight = molecular_weight(mod_seqeunce, seq_type='protein')
    weight = weight + 110*ambigous_count  # Estimate
    return weight


def kegggene_to_uniprotid(organism, kegggene):
    "Kegg gene to Uniprot ID"
    text = REST.kegg_get(organism.lower() + ':' + kegggene).read()
    uni_index = text.find('UniProt')

    if uni_index != -1:
        return text[uni_index + 9: uni_index + 15]
    else:
        return None
