
.PHONY: setup database sync

all: setup

setup: virtualenv requirements

virtualenv:
	virtualenv --python python3 venv

requirements:
	venv/bin/pip install -r requirements.txt

database:
	venv/bin/beam config --as-json --site src/index.yml > database.json

sync:
	venv/bin/python .script/sync.py
