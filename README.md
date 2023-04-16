# ChatGPT clone

This is a clone of ChatGPT using [Open Assistant](https://huggingface.co/OpenAssistant).

## Dependencies

- Docker
- Docker Compose

To run the model on GPU, you will also need:

- Nvidia Docker
- Nvidia GPU with at least 24GB of memory

## Instructions

Create a `.env` file in [ui](./ui) with the API URL (by default you can use `http://localhost:8000` by renaming `.env.example` to `.env`).

Build the docker images

```
docker-compose build
```

Start the docker containers

```
docker-compose up
```

The API will be available at [http://localhost:8000](http://localhost:8000), with interactive docs at [http://localhost:8000/docs](http://localhost:8000/docs). Check the logs since it may take some time to download the model and load everything.

The UI will be available at [http://localhost:5173](http://localhost:5173).

![pic](pic.png)

You can modify the number of GPUs available in the `docker-compose.yml` file.
