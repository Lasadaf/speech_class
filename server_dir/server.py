from fastapi import FastAPI, Response, Request
from pydantic import BaseModel
import json
import shutil
import os
import time
import predict

class WAVInfo(BaseModel):
    text:str

app = FastAPI()

@app.get("/")
async def root():
    file_list = os.listdir("../recipe/model/")
    model_list = []
    for f in file_list:
        name = f.split(".")
        if len(name) > 1 and name[-1] == "joblib":
            model_list.append(f)
    data = json.dumps(model_list)
    print("Sending list of models:")
    print(data)
    return Response(content=data, media_type="text/plain")

@app.post("/")
async def get_wav(request:Request):
    print("Recieved something")
    js = await request.json()
    #print("actually got:")
    #print(js)
    #data = json.loads(json.dumps(js))
    tmp = "./server_files/" + js['uid']
    os.mkdir(tmp)
    with open(tmp + '/myfile.wav', mode='bx') as f:
        f.write(bytearray(js['bytes']))
    print("Pretend this is getting analysed...")
    
    probas = predict.predict(tmp, js['model'])

    data = json.dumps(probas)
    print("Sending back:")
    print(data)
    print("Analisys complete...")
    shutil.rmtree(tmp)
    return Response(content=data, media_type="text/plain")


