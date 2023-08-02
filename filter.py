#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
logging.basicConfig(format='%(asctime)s : %(filename)s : %(levelname)s : %(message)s')
logger = logging.getLogger()

import sys
import json
from time import time as now
import pydash
import signal
import traceback
from time import time as now

def is_person(rec):
  return pydash.has(rec, 'claims.P31') and pydash.get(rec, 'claims.P31[0].mainsnak.datavalue.value.id') == 'Q5'

def is_taxon(rec):
  return pydash.has(rec, 'claims.P31') and pydash.get(rec, 'claims.P31[0].mainsnak.datavalue.value.id') == 'Q16521'

def is_location(rec):
  return pydash.has(rec, 'claims.P625')

if __name__ == '__main__':
  import argparse
  parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter, description=__doc__)
  parser.add_argument('--log', help='Logging level (default=warning)', default='warning')

  parser.add_argument('-p', '--people', action='store_true', help='Filter wikidata entities for people')
  parser.add_argument('-t', '--taxons', action='store_true', help='Filter wikidata entities for taxon entities')
  parser.add_argument('-l', '--locations', action='store_true', help='Filter wikidata entities for locations')

  args = parser.parse_args()
  
  if args.log == 'debug': logger.setLevel(logging.DEBUG)
  if args.log == 'info': logger.setLevel(logging.INFO)
  if args.log in ('warning', 'warn') : logger.setLevel(logging.WARNING)
  if args.log == 'error': logger.setLevel(logging.ERROR)
  
  def SIGINT_handler(signal, frame):
    pass # Ignore SIGINT (Ctrl+C) signals
  signal.signal(signal.SIGINT, SIGINT_handler)
  
  ctr = 0
  start = now()
  for idx, line in enumerate(sys.stdin):
    try:
      rec = json.loads(line)
      if args.people and is_person(rec) or \
         args.taxons and is_taxon(rec) or \
         args.locations and is_location(rec):
        ctr += 1
        print(json.dumps(rec))
      
      if idx > 0 and idx % 100000 == 0:
        pct = round(100*ctr/idx, 2) if idx > 0 else 0
        logger.info(f'{ctr:,d}/{idx:,d} ({pct}%) {round(idx/(now()-start)):,d}/sec')
        
    except KeyboardInterrupt:
      logger.info('KeyboardInterrupt')
      break
    except:
      logger.warning(traceback.format_exc())
      logger.warning(line)

  logger.info(f'{ctr:,d}/{idx:,d} {round(idx/(now()-start)):,d}/sec')
