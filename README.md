# Wikidata dumpfile utilities

Simple utility programs for processing Wikidata dump files.

## Setup

### Create and activate python virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Add dependencies

```bash
pip install -r requirements.txt
```

## Run simple pipeline

Prints the QID and label for all people found in the first 100 entities in the dump file

```bash
./read.py --limit 100 | ./filter.py --people | ./transform.py
```
