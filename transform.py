#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
logging.basicConfig(format='%(asctime)s : %(filename)s : %(levelname)s : %(message)s')
logger = logging.getLogger()

import sys
import json
import pydash
import signal
import traceback

if __name__ == '__main__':
  import argparse
  parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter, description=__doc__)
  parser.add_argument('--log', help='Logging level (default=warning)', default='warning')
  args = parser.parse_args()
  
  if args.log == 'debug': logger.setLevel(logging.DEBUG)
  if args.log == 'info': logger.setLevel(logging.INFO)
  if args.log in ('warning', 'warn') : logger.setLevel(logging.WARNING)
  if args.log == 'error': logger.setLevel(logging.ERROR)
  
  def SIGINT_handler(signal, frame):
    pass # Ignore SIGINT (Ctrl+C) signals
  signal.signal(signal.SIGINT, SIGINT_handler)
  
  for line in sys.stdin:
    try:
      rec = json.loads(line)
      qid = pydash.get(rec, 'id')
      label = pydash.get(rec, 'labels.en.value')
      sys.stdout.write(f'{qid} {label}\n')
    except:
      logger.warning(traceback.format_exc())
      logger.warning(line)
