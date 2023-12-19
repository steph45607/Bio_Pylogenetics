# from datetime import date, timedelta, datetime
# from typing import Union, Optional
from fastapi import Depends, FastAPI, HTTPException, status, Response, BackgroundTasks
from pydantic import BaseModel
from typing_extensions import Annotated
from fastapi.middleware.cors import CORSMiddleware
from pydantic import ValidationError
import io
import matplotlib
matplotlib.use('AGG')
import matplotlib.pyplot as plt
import base64
import numpy as np
from fastapi import UploadFile, File
import aiofiles
from Bio import AlignIO, SeqIO, pairwise2, Phylo
import numpy as np
from scipy.cluster import hierarchy
import matplotlib.pyplot as plt
import time
import tracemalloc
from Bio.Phylo.TreeConstruction import DistanceCalculator, DistanceTreeConstructor


app = FastAPI()

origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def create_img():
    x = np.linspace(0, 2 * np.pi, 100)
    y = np.sin(x)

    plt.plot(x, y)
    plt.title('Sine Wave')
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')

    img_buf = io.BytesIO()
    plt.savefig(img_buf, format='png')
    plt.close()

    img_base64 = base64.b64encode(img_buf.getvalue()).decode('utf-8')
    img_buf.close()
    return img_base64

def align_local(seqi, seqii, match, mismatch, open_gap, gap):

    c_seqi = np.array(list(seqi.seq))
    c_seqii = np.array(list(seqii.seq))

    ni = len(c_seqi)
    nii = len(c_seqii)

    # Initialize the Smith-Waterman matrix

    M = np.zeros((ni + 1, nii + 1))

    # Compute the Smith-Waterman matrix

    for i in range(1, ni + 1):
        for j in range(1, nii + 1):
            diag = M[i - 1, j - 1]
            ver = M[i - 1, j]
            hor = M[i, j - 1]
            diag += match if (c_seqi[i - 1] == c_seqii[j - 1]) else mismatch
            ver += open_gap if (i == 1) else gap
            hor += open_gap if (j == 1) else gap
            M[i, j] = max([diag, ver, hor, 0])

    # Find the optimal local alignment
    i, j = np.unravel_index(M.argmax(), M.shape)
    al_seqi = []
    al_seqii = []

    while i > 0 and j > 0 and M[i, j] > 0:
        diag = M[i - 1, j - 1]
        ver = M[i - 1, j]
        hor = M[i, j - 1]
        

        if diag >= ver and diag >= hor:
            i -= 1
            j -= 1
            al_seqi.append(c_seqi[i])
            al_seqii.append(c_seqii[j])

        elif hor > diag and hor > ver:
            j -= 1
            al_seqii.append(c_seqii[j])
            al_seqi.append('-')


        elif ver > diag and ver > hor:
            i -= 1
            al_seqi.append(c_seqi[i])
            al_seqii.append('-')
            
            
    al_seqi = [''.join(al_seqi)[::-1], seqi.id]
    al_seqii = [''.join(al_seqii)[::-1], seqii.id]

    pair = [al_seqi, al_seqii]
    # print("pair", pair)
    return pair

def needleman_wunsch(seq1, seq2):
    #? m = match score of identical chars
    #? s = open and extend gap penalty for both sequences
    #? parameters = (seq1, seq1, match, mismatch, opening a gap, extending a gap)
    #// scores from https://en.wikipedia.org/wiki/Needleman%E2%80%93Wunsch_algorithm 
    alignment = pairwise2.align.globalms(seq1.seq, seq2.seq, 2,-1,-5,-1)
    # print(alignment[0].seqA)
    # change = []
    # notchange = []
    change = 0

    if alignment[0].seqA == seq1.seq:
        # notchange.append([alignment[0].seqA, seq1.id])
        pass
    else:
        change=[alignment[0].seqA, seq1.id]

    if alignment[0].seqB == seq2.seq:
        # notchange.append([alignment[0].seqB, seq2.id])
        pass
    else:
        change=[alignment[0].seqB, seq2.id]
    print("change", change)
    # print("nochange", notchange)
    # pair = [alignment[0].seqA, seq1.id]
    
    if change is None:
        pass
    else:
        return change
    # return change

def readFasta():
    seq = []
    for i in SeqIO.parse("phylo/src/algo/out.fasta", "fasta"):
        # print(i)
        seq.append(i)
    return seq

def makeFastaNW(seq):

    num_seqs = len(seq)
    print(num_seqs)

    alignment = []

    for i in range(num_seqs):
        for j in range(i+1, num_seqs):
            alignment.append(needleman_wunsch(seq[i], seq[j]))
    
    while 0 in alignment:
        alignment.remove(0)
    
    print(alignment)

    final = []
    final_seq = []


    for i in reversed(range(len(alignment))):
        if alignment[i][1] in final:
            pass
        else:
            final.append(alignment[i][1])
            final_seq.append(alignment[i][0])
    
    print(final)
    print(final_seq)

    for i in seq:
        if i.id in final:
            pass
        else:
            final.append(i.id)
            final_seq.append(str(i.seq))

    print("final", final)
    print("final_seq", final_seq)

    file = open("41ign.fasta", "w")
    for i in range(len(final)):
        file.write(">"+final[i]+"\n"+final_seq[i]+"\n")
    file.close()

    return phylo()

def makeFastaSW(seq):

    num_seqs = len(seq)
    print(num_seqs)

    alignment = []
    aligns = []
    aligned = []
    # print("test")
    # print(seq[0].seq)

    for i in range(num_seqs):
        for j in range(i+1, num_seqs):
            alignment.append(align_local(seq[i], seq[j], 2, -1, -2, -1))
    
    # print("ALINGMENT", alignment)
    for i in alignment:
            aligns.append(i[1])

    aligns.insert(0, alignment[0][0])
    # print("ALIGNS", aligns)

    ml = 0
    for i in aligns:
        if len(i[0]) > ml:
            ml = len(i[0])
        
    for i in aligns:
        if len(i[0]) < ml:
            i[0] = i[0] + "-" * (ml - len(i[0]))
            aligned.append(i)
        else:
            aligned.append(i)

    print("")
    print("ALIGNED", aligned)

    final = []
    final_seq = []

    for i in reversed(range(len(aligned))):
        if aligned[i][1] in final:
            pass
        else:
            final.append(aligned[i][1])
            final_seq.append(aligned[i][0])
    
    print("final", final)
    print("final_seq", final_seq)

    file = open("41ign.fasta", "w")
    for i in range(len(final)):
        file.write(">"+final[i]+"\n"+final_seq[i]+"\n")
    file.close()
    phylo()

def phylo():
    align = AlignIO.read("41ign.fasta", "fasta")
    calc = DistanceCalculator('identity')
    dist = calc.get_distance(align)
    construct = DistanceTreeConstructor()
    tree = construct.nj(dist)

    fig = plt.figure(figsize=(10, 20), dpi=100)
    axes = fig.add_subplot(1, 1, 1)
    Phylo.draw(tree)
    plt.show()

    img_buf = io.BytesIO()
    plt.savefig(img_buf, format='png')
    plt.close()

    img_base64 = base64.b64encode(img_buf.getvalue()).decode('utf-8')
    img_buf.close()
    return img_base64
    # plt.savefig('phyl0.png')
    
@app.get('/getimage')
async def get_img(background_tasks: BackgroundTasks):
    img_base64 = create_img()
    return {"image": img_base64}

@app.post('/uploadnw')
async def upload(file: UploadFile):
    # saving the file into local fine out.fasta
    async with aiofiles.open("phylo/src/algo/out.fasta", "wb") as out:
        while content := await file.read(1024):
            await out.write(content)
    # run the test function
    # makeFastaNW(readFasta())
    img = makeFastaNW(readFasta())
    return {"image": img}

@app.post('/uploadsw')
async def upload(file: UploadFile):
    # saving the file into local fine out.fasta
    async with aiofiles.open("phylo/src/algo/out.fasta", "wb") as out:
        while content := await file.read(1024):
            await out.write(content)
    # run the test function
    makeFastaSW(readFasta())
    return "ok"
