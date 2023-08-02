#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
logging.basicConfig(format='%(asctime)s : %(filename)s : %(levelname)s : %(message)s')
logger = logging.getLogger()

import bz2
import os
import sys
import signal
from time import time as now

filepos = 0
ct = 0
done = False

default_dumpfile = f'./latest-all.json.bz2'

def wikidata(path):
  global filepos, done
  with bz2.open(path, mode='rt') as f:
    f.read(filepos) 
    while not done:
      line = f.readline()
      filepos = f.tell()
      if line: yield line
      else: done = True

if __name__ == '__main__':
  import argparse
  parser = argparse.ArgumentParser( formatter_class=argparse.ArgumentDefaultsHelpFormatter, description=__doc__)
  parser.add_argument('--path', help='Wikidata dumpfile (bz2)', default=default_dumpfile)
  parser.add_argument('--log', help='Logging level (default=warning)', default='warn')
  parser.add_argument('--resume', help='Seek to file position')
  parser.add_argument('--limit', help='Max records to read', type=int, default=-1)
  args = parser.parse_args()
  
  if args.log == 'debug': logger.setLevel(logging.DEBUG)
  if args.log == 'info': logger.setLevel(logging.INFO)
  if args.log in ('warning', 'warn') : logger.setLevel(logging.WARNING)
  if args.log == 'error': logger.setLevel(logging.ERROR)
  
  ctr, filepos = [int(v) for v in args.resume.split(':')] if args.resume else [0, 2] if args.path == default_dumpfile else [0 , 0]
  if ctr > 0: ctr = ctr - 1
  limit = args.limit + ctr if args.limit > 0 else None
  
  
  rec = None

  def SIGINT_handler(signal, frame):
    global done
    done = True
  signal.signal(signal.SIGINT, SIGINT_handler)
  
  start = now()
  for raw in wikidata(args.path):
    ctr = ctr+1
    sys.stdout.write(raw.rstrip(',\n') + '\n')
    if limit and ctr >= limit: done = True
    if done: sys.stdout.flush()
    if ctr > 0 and ctr % 100000 == 0:
      logger.info(f'{ctr:,d} ({round(ctr/(now()-start)):,d}/s)')
  
  sys.stdout.flush()
  sys.stderr.write(f'Entities read: {ctr:,d} ({round(ctr/(now()-start)):,d}/sec) resume={ctr+1}:{filepos}\n')
