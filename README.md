### Instructions to setup fastapi server with multiple workers for embedding creation

1. create a conda environment and install `ems_requirements.txt` inside the environment.
2. install the below commands inside conda environment 
```
python embedding_model_server.py --workers 2 --gpus 2 --modelname all-MiniLM-L6-v2
```
---
