#!/bin/python

import os
import sys
import logging
import argparse
from loader.loader import build_loader


def set_up_logging():
    if args.verbose:
        logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)
    else:
        logging.basicConfig(format='%(asctime)s %(message)s', level=logging.WARN)


def set_up_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("urls", help="the file containing the list of source urls")
    parser.add_argument("-d", "--dir", type=str, default=os.getcwd(),
                        help="the output directory (default: current working directory)")
    parser.add_argument("--continue-on-error", action="store_true", dest="continue_on_error", default=False,
                        help="let {} continue if one url download fails (default: false)".format(sys.argv[0]))
    parser.add_argument("-v", "--verbose", action="store_true", default=False, help="verbose output")
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = set_up_arguments()
    set_up_logging()
    loader = build_loader(args.urls, args.dir)

    success = loader.start(continue_on_error=args.continue_on_error)
    if not success:
        exit(1)
