from src.stress import Stress
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import os
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI()
Instrumentator().instrument(app).expose(app)

class CPURequest(BaseModel):
    stress_time : int
    cores_n : int

@app.post('/cpu-stress')
def cpu_stress(r : CPURequest):
    h = Stress()
    h.cpu_stress(r.stress_time, r.cores_n)
    return {f'cpu stressed for {r.stress_time} seconds'}

class MemoryRequest(BaseModel):
    stress_time : int
    bytes_n : int

@app.post('/memory-stress')
def memory_stress(r : MemoryRequest):
    h = Stress()
    h.memory_stress(r.stress_time, r.bytes_n)
    return {f'memory stressed for {r.stress_time} seconds'}
    

if __name__ == '__main__':
    host = os.environ['APP_HOST']
    port = int(os.environ['APP_PORT'])
    uvicorn.run(app, host=host, port=port)