# Author: Bostjan Cigan
# https://bostjan-cigan.com
 
from Bio import Entrez
from Bio import SeqIO
import pylab
from scipy.cluster.hierarchy import linkage, dendrogram
import numpy as np
 
# Key = organism ID
# Value = Name, COX3
organisms = {
    'NC_000845.1':['Wild bore'],
    'NC_001640.1':['Horse'],
    'AC_000022.2':['Brown rat'],
    'NC_001643.1':['Chimpanzee'],
    'NC_001645.1':['Gorilla'],
    'NC_002008.4':['Dog'],
    'NC_002083.1':['Orangutan'],
    'NC_004299.1':['Fugu rubripes'],
    'NC_006580.1':['Goldfish'],
    'NC_011137.1':['Neanderthal'],
    'NC_011391.1':['Russels viper'],
    'NC_012061.1':['Dolphin'],
    'NC_012420.1':['Chameleon'],
    'NC_012920.1':['Human']
}
 
organisms_table = [
    'NC_000845.1',
    'NC_001640.1',
    'AC_000022.2',
    'NC_001643.1',
    'NC_001645.1',
    'NC_002008.4',
    'NC_002083.1',
    'NC_004299.1',
    'NC_006580.1',
    'NC_011137.1',
    'NC_011391.1',
    'NC_012061.1',
    'NC_012420.1',
    'NC_012920.1'
]
 
names = [
    'Wild bore',
    'Horse',
    'Brown rat',
    'Chimpanzee',
    'Gorilla',
    'Dog',
    'Orangutan',
    'Fugu rubripes',
    'Goldfish',
    'Neanderthal',
    'Russels viper',
    'Dolphin',
    'Chameleon',
    'Human'
]
 
# Read COX3 data
def prepare_data():
    for organism, data in organisms.items():
        handle = Entrez.efetch(db="nucleotide", rettype="gb", id=organism, email='a@gmail.com')
        rec = SeqIO.read(handle, "gb")
        handle.close()
        for f in rec.features:
            if f.type == "CDS":
                if f.qualifiers["gene"][0] == "COX3":
                    cox3 = f.qualifiers["translation"][0]
                    data = organisms[organism]
                    data.append(cox3)
                    organisms[organism] = data
 
# Read the BLOSUM50 table
def read_BLOSUM50(fname):
    d = {}
    lines = open(fname, "rt").readlines()
    alpha = lines[0].rstrip('\n\r').split()
    assert(len(alpha) == len(lines)-1)
    for r in lines[1:]:
        r = r.rstrip('\n\r').split()
        a1 = r[0]
        for a2, score in zip(alpha, r[1:]):
            d[(a1, a2)] = int(score)
    return d
 
def needleman_wunsch(seq1, seq2, blosum, pen):
 
    m = len(seq1)+1 # Rows
    n = len(seq2)+1 # Columns
 
    M = create_matrix(m, n)
 
    for i in range(0, m):
        M[i][0] = i * pen
    for j in range(0, n):
        M[0][j] = j * pen
 
    for i in range(1, m):
        for j in range(1, n):
            match = M[i-1][j-1] + blosum[(seq1[i-1], seq2[j-1])]
            delete = M[i-1][j] + pen
            insert = M[i][j-1] + pen
            M[i][j] = max(match, delete, insert)
 
    return M
 
# Create an empty matrix
def create_matrix(m, n):
    return [[0]*n for _ in range(m)]
 
# Calculate the scoring matrix between organisms
def scoring_matrix(organisms_table, blosum):
 
    scoring_matrix = create_matrix(len(organisms_table), len(organisms_table))
 
    i = 0
    for x in organisms_table:
        j = 0
        for y in organisms_table:
            M = needleman_wunsch(organisms[x][1], organisms[y][1], blosum, -5) 
            scoring_matrix[i][j] = M[-1][-1]
            j = j + 1
        i = i + 1
 
    return scoring_matrix   
 
# Calculate the distance scoring matrix
def scoring_distance_matrix(scoring_matrix):
 
    scoring_distance_matrix = create_matrix(len(scoring_matrix[0]), len(scoring_matrix[0]))
    maxR = get_matrix_max(scoring_matrix)
 
    for i in range(0, len(organisms_table)):
        for j in range(0, len(organisms_table)):
            scoring_distance_matrix[i][j] = abs(scoring_matrix[i][j] - maxR)
 
    return scoring_distance_matrix
 
# Return the max value in a matrix, used in 
# scoring_distance_matrix method
def get_matrix_max(matrix):
 
    max_value = None
 
    for i in range(0, len(matrix[0])):
        for j in range(0, len(matrix[0])):
            if(max_value == None):
                max_value = matrix[i][j]
            if(matrix[i][j] >= max_value):
                max_value = matrix[i][j]
 
    return max_value
 
d = read_BLOSUM50("phylo/src/algo/BLOSUM50.txt")
prepare_data()
scoring = scoring_matrix(organisms_table, d)
scoring_distance_matrix = scoring_distance_matrix(scoring)
average = linkage(scoring_distance_matrix, "average")
dendrogram(average, labels=names, orientation="left", leaf_font_size=8)
# pylab.subplots_adjust(bottom=0.1, left=0.2, right=1.0, top=1.0)
pylab.savefig("dendro.jpg")