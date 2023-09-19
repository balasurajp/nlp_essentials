from concurrent.futures import ProcessPoolExecutor
import traceback
from typing import Callable
from fastapi import FastAPI
from torch import embedding
app = FastAPI()

def create_model():
    # Your model creation logic
    model = None
    return model
app_model = create_model()

@app.get("/get_embedding")
async def get_embedding(payload):
    global app_model
    text = str(payload.text)
    
    try:
        # Your embedding logic here
        # embedding = app_model(text)
        response = None
        status = 'success'
    except:
        response = traceback.format_exc()
        status = 'failed'

    return {'status': status, "embedding": response, "text": text}

def run_worker(gpu_id):
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000 + gpu_id)

if __name__ == "__main__":
    num_workers_per_gpu = 2
    num_gpus = 4

    with ProcessPoolExecutor() as executor:
        for gpu_id in range(num_gpus):
            for _ in range(num_workers_per_gpu):
                executor.submit(run_worker, gpu_id)
