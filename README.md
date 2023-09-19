### Instructions to setup NGINX load balancer for multiple fastapi servers

1. create a conda environment and install `nlb_requirements.txt` inside the environment.
2. install the below commands in 
```
sudo apt-get update
sudo apt-get install nginx
```
3. run the following commands to start nginx reverse proxy load balancing server
```
python embedding_model_server.py
python nginx_load_balancer.py
[RUN COMMANDS PRINTED IN TERMINAL]
```
---
