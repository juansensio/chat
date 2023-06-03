FROM nvidia/cuda:11.6.2-base-ubuntu20.04

RUN apt-get update && \
    apt-get install -y python3-pip
	
RUN pip install fastapi 
RUN pip install uvicorn
RUN pip install	torch --index-url https://download.pytorch.org/whl/cu118
RUN pip install transformers
RUN pip install accelerate
RUN pip install einops