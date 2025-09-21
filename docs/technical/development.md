# Before anything (activate the project) if you don't see (venv) in prompt
source venv/bin/activate

# To start the app
sh working.sh (To exit use ctrl+c)

# To install new dependencies (assuming new dependendencies are in requirements.txt)
# add dependency to requirements.txt
pip install -r requirements.txt



tmux new -s jupyter
source venv/bin/activate
jupyter lab \
    --no-browser \
    --ip=0.0.0.0 \
    --port=8888 \
    --allow-root \
    --NotebookApp.token='48LpdLb5v~+AhAdkhC' \
    --NotebookApp.password='Y8qFN@Vd3U.*=cy}d5cj' \
    --NotebookApp.allow_origin='*'
(Then use ctrl+b) (then press key b)

http://34.171.12.47:8888/tree?token=48LpdLb5v~+AhAdkhC

# SSH para conectar el cliente a la BD
export DB_HOST=localhost
export DB_PORT=3306
export DB_USERNAME=alvaro
export DB_PASSWORD=n8PUqbXXA6pBYGjdvx7Z
export DB_NAME=ennui_rag