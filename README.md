Get the docker image for ollama

`docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama`

Run the container, this will automatically pull the defined model into the local folder.
`docker exec -it ollama ollama pull llama3.2`


`
