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

def smith_waterman_distance(seq1, seq2):
    #? m = match score of identical chars
    #? s = open and extend gap penalty for both sequences
    #? parameters = (seq1, seq1, match, mismatch, opening a gap, extending a gap)
    #// scores from https://gist.github.com/radaniba/11019717 
    alignment = pairwise2.align.localms(seq1.seq, seq2.seq, 2, -1, -1, -1)
    #? gap score
    # score = alignment[0].score
    # return len(seq1) + len(seq2) - score * 2
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
    tracemalloc.start()
    start = time.time()

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
    phylo()

def makeFastaSW(seq):
    tracemalloc.start()
    start = time.time()

    num_seqs = len(seq)
    print(num_seqs)

    alignment = []
    # print("test")
    # print(seq[0].seq)

    for i in range(num_seqs):
        for j in range(i+1, num_seqs):
            alignment.append(smith_waterman_distance(seq[i], seq[j]))
            # alignment.append(needleman_wunsch(sequences[i], sequences[j])[0].seqB)
    # print(alignment)

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
    plt.savefig('phyl0.png')
    
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
    makeFastaNW(readFasta())
    return "ok"

@app.post('/uploadsw')
async def upload(file: UploadFile):
    # saving the file into local fine out.fasta
    async with aiofiles.open("phylo/src/algo/out.fasta", "wb") as out:
        while content := await file.read(1024):
            await out.write(content)
    # run the test function
    makeFastaSW(readFasta())
    return "ok"
