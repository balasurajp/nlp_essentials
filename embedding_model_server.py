import traceback, argparse
import uvicorn
import torch
from sentence_transformers import SentenceTransformer, util
from pydantic import BaseModel
from typing import List, Any
from fastapi import FastAPI
from itertools import cycle

# Create a FastAPI app
app = FastAPI()
model_name = "all-MiniLM-L6-v2"
model_workers = {
    'worker1': SentenceTransformer(model_name, device='cuda:0' if torch.cuda.is_available() else 'cpu')
}
round_robin_balancer = cycle(['worker1'])

# Create multiple identical sentence transformer models
def create_model(num_workers:int, num_gpus:int):
    global model_name
    global model_workers
    global round_robin_balancer

    model_workers = {}
    model_worker_names = []
    for worker_num in range(num_workers):
        try:
            model = SentenceTransformer(model_name, device=f'cuda:{worker_num%num_gpus}')
            model_workers[f"worker{worker_num+1}"] = model
            model.encode(['test sample'])
            model_worker_names.append(f"worker{worker_num+1}")
            print(f"{model_name} has been created successfully as worker{worker_num+1} - {model}")
        except Exception:
            print(f"{model_name} has not been created as worker{worker_num+1}\n\n{'='*10}{traceback.format_exc()}{'='*10}")
    print(model_workers)
    round_robin_balancer = cycle(model_worker_names)

def get_embedding_using_worker(model_worker_name:str, embedding_text: str) -> List[Any]:
    global model_workers
    current_model:SentenceTransformer = model_workers[model_worker_name]
    embedding_vector= list(current_model.encode([embedding_text], normalize_embeddings=True)[0].tolist())
    return embedding_vector

# define the main 'get_embedding' endpoint
@app.get("/get_embedding")
async def get_embedding(embedding_text:str):

    # Get the next worker function using round-robin strategy
    global round_robin_balancer
    worker_name = next(round_robin_balancer)

    #  selected model worker and create embedding for payload text
    embedding_vector =  get_embedding_using_worker(worker_name,embedding_text)
    return {
        "model_name": model_name, 
        'embedding_text':embedding_text, 
        "embedding_vector":embedding_vector
    }

# Run the FastAPI app
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='FastAPI Server with Embedding Model')
    parser.add_argument('--modelname', type=str, default="all-MiniLM-L6-v2")
    parser.add_argument('--gpus', type=int, default=1)
    parser.add_argument('--workers', type=int, default=1)
    args = parser.parse_args()

    model_name = str(args.modelname)
    create_model(args.workers, args.gpus)

    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)