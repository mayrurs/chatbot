Get the docker image for ollama

`docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama`

Run the container, this will automatically pull the defined model into the local folder.
`docker exec -it ollama ollama pull llama3.2`

**Remark**: If there is an issue to pull the model from the container. Ollama can be 
installed directly on the machine with `curl -fsSL https://ollama.com/install.sh | sh` for Ubuntu.

Create a python virual environment
`python3 -m venv venv`

Install the dependencies
`pip install -r requirements`

Start the frontend application
`streamlit run chatbot.py`
`
