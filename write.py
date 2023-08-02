#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
logging.basicConfig(format='%(asctime)s : %(filename)s : %(levelname)s : %(message)s')
logger = logging.getLogger()

import bz2
import json
import signal
import sys

if __name__ == '__main__':
  import argparse
  parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter, description=__doc__)
  parser.add_argument('--log', help='Logging level (default=warning)', default='warning')
  parser.add_argument('--out', help='Output destination', default='stdout')
  args = parser.parse_args()
  
  if args.log == 'debug': logger.setLevel(logging.DEBUG)
  if args.log == 'info': logger.setLevel(logging.INFO)
  if args.log in ('warning', 'warn') : logger.setLevel(logging.WARNING)
  if args.log == 'error': logger.setLevel(logging.ERROR)
  
  def SIGINT_handler(signal, frame):
    pass # Ignore SIGINT (Ctrl+C) signals
  signal.signal(signal.SIGINT, SIGINT_handler)
  
  outfile = bz2.open(args.out, 'wt') if args.out.endswith('bz2') else None

  rec = None
  for idx, line in enumerate(sys.stdin):
    try:
      if args.out == 'stdout':
        sys.stdout.write(line)
      elif outfile:
        outfile.write(line)
    except json.decoder.JSONDecodeError:
      logger.warning(f'JSONDecodeError: {line}')

  if outfile: outfile.close()
  