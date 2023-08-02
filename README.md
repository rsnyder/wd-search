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

This pipeline prints the QID and label for all people found in the first 100 entities in the dump file.  The Wikidata dump file is assumed to reside in the current directory in the file `latest-all.json.bz2`.  If the dump file is located elsewhere the `--path` argument must be used to specify the location. 

```bash
./read.py --limit 100 | ./filter.py --people | ./transform.py
```
