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
    
@app.get('/getimage')
async def get_img(background_tasks: BackgroundTasks):
    img_base64 = create_img()
    return {"image": img_base64}