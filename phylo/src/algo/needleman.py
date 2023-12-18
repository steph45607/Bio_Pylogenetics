# source = https://wilkelab.org/classes/SDS348/2019_spring/labs/lab13-solution.html
from Bio import Phylo, AlignIO, SeqIO
from Bio.Phylo.TreeConstruction import DistanceCalculator, DistanceTreeConstructor
# from tabulate import tabulate
gap = -1
match = 1
mismatch = -1

p1 = SeqIO.read("phylo/src/algo/duck.fasta", "fasta")
p2 = SeqIO.read("phylo/src/algo/homo_sapiens.genome.fasta", "fasta")
# p3 = SeqIO.read("phylo/src/algo/asastrepha.fasta", "fasta")

a = p1.seq
b = p2.seq



# make empty matrix
def matrix(rows, columns):
    matrix = []
    for i in range(rows):
        matrix.append([])
        for j in range(columns):
            matrix[-1].append(0)

    return matrix

# scoring
def match_score(a,b):
    if a == b:
        return match
    elif a == '-' or b == '-':
        return gap
    else:
        return mismatch

# algo
def needleman_wunsch(seq1, seq2):
    
    # Store length of two sequences
    n = len(seq1)  
    m = len(seq2)
    
    # Generate matrix of zeros to store scores
    score = matrix(m+1, n+1)
   
    # Calculate score table
    
    # Fill out first column
    for i in range(0, m + 1):
        score[i][0] = gap * i
    
    # Fill out first row
    for j in range(0, n + 1):
        score[0][j] = gap * j
    
    # Fill out all other values in the score matrix
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            # Calculate the score by checking the top, left, and diagonal cells
            match = score[i - 1][j - 1] + match_score(seq1[j-1], seq2[i-1])
            delete = score[i - 1][j] + gap
            insert = score[i][j - 1] + gap
            # Record the maximum score from the three possible scores calculated above
            score[i][j] = max(match, delete, insert)
    
    # Traceback and compute the alignment 
    
    # Create variables to store alignment
    align1 = ""
    align2 = ""
    
    # Start from the bottom right cell in matrix
    i = m
    j = n
    
    # We'll use i and j to keep track of where we are in the matrix, just like above
    while i > 0 and j > 0: # end touching the top or the left edge
        score_current = score[i][j]
        score_diagonal = score[i-1][j-1]
        score_up = score[i][j-1]
        score_left = score[i-1][j]
        
        # Check to figure out which cell the current score was calculated from,
        # then update i and j to correspond to that cell.
        if score_current == score_diagonal + match_score(seq1[j-1], seq2[i-1]):
            align1 += seq1[j-1]
            align2 += seq2[i-1]
            i -= 1
            j -= 1
        elif score_current == score_up + gap:
            align1 += seq1[j-1]
            align2 += '-'
            j -= 1
        elif score_current == score_left + gap:
            align1 += '-'
            align2 += seq2[i-1]
            i -= 1

    # Finish tracing up to the top left cell
    while j > 0:
        align1 += seq1[j-1]
        align2 += '-'
        j -= 1
    while i > 0:
        align1 += '-'
        align2 += seq2[i-1]
        i -= 1
    
    # Since we traversed the score matrix from the bottom right, our two sequences will be reversed.
    # These two lines reverse the order of the characters in each sequence.
    align1 = align1[::-1]
    align2 = align2[::-1]
    # print(score)
    # print(len(score))

    # for i in range(len(score)):
    #     print("\n")
    #     for j in range(len(score[i])):
    #         print(score[i][j], " ", end="")

    # a = [*seq1]
    # print(tabulate(score, headers=a))


    return(align1, align2)

output1, output2 = needleman_wunsch(a, b)

print(output1 + "\n" + output2)