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
from Bio import AlignIO, SeqIO
import numpy as np
from Bio import pairwise2
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
    alignment = pairwise2.align.localms(seq1, seq2, 2, -1, -1, -1)
    #? gap score
    print("align = ", alignment)
    print("==============")
    score = alignment[0].score
    return len(seq1) + len(seq2) - score * 2

def readFasta():
    seq = []
    for i in SeqIO.parse("phylo/src/algo/out.fasta", "fasta"):
        # print(i.seq)
        seq.append(i.seq)
    return seq

def main(seq):
    # print(seq)
    tracemalloc.start()
    start = time.time()
    sequences = seq

    num_seqs = len(sequences)
    distance_matrix = np.zeros((num_seqs, num_seqs))
    print("1")
    for i in range(num_seqs):
        for j in range(i + 1, num_seqs):
            distance = smith_waterman_distance(sequences[i], sequences[j])
            distance_matrix[i][j] = distance
            distance_matrix[j][i] = distance
    print("2")
    # print(distance_matrix)
    #// Perform hierarchical clustering (UPGMA)
    #// Inspiration from https://www.researchgate.net/figure/Phylogenetic-tree-using-UPGMA-method_fig1_325228699 
    link = hierarchy.linkage(distance_matrix, method='average')
    end = time.time()
    mem = tracemalloc.get_traced_memory()
    print(f"Time = {end-start}")
    print(f"memory = {mem[0]}")

    # construct = DistanceTreeConstructor()
    # tree = construct.nj(distance_matrix)
    # Phyo.draw(tree)

    #// Plot the phylogenetic tree
    #// https://codinginfinite.com/plot-dendrogram-in-python/
    plt.figure(figsize=(8, 6),num="Smith-Waterman")
    dendrogram = hierarchy.dendrogram(link, labels=sequences, leaf_rotation=-75, leaf_font_size=6)
    plt.xlabel('Sequence Index')
    plt.ylabel('Distance')
    plt.title('Phylogenetic Tree')
    plt.savefig("result.png")
    
@app.get('/getimage')
async def get_img(background_tasks: BackgroundTasks):
    img_base64 = create_img()
    return {"image": img_base64}

@app.post('/upload')
async def upload(file: UploadFile):
    # saving the file into local fine out.fasta
    async with aiofiles.open("phylo/src/algo/out.fasta", "wb") as out:
        while content := await file.read(1024):
            await out.write(content)
    # run the test function
    main(readFasta())
    return "ok"

