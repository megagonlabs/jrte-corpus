#!/usr/bin/env python3

import argparse
import sys


def get_opts() -> argparse.Namespace:
    oparser = argparse.ArgumentParser()
    oparser.add_argument("--op", required=True)
    oparser.add_argument("--source", required=True)
    oparser.add_argument("--data", required=True)
    return oparser.parse_args()


def main() -> None:
    opts = get_opts()
    source_ids = set()
    with open(opts.source) as sf:
        for line in sf:
            source_ids.add(line.split('\t')[0])

    data_ids = set()
    with open(opts.op) as inf:
        for line in inf:
            sid = line.split('\t')[1]
            did = line.split('\t')[0]
            data_ids.add(did)
            if sid not in source_ids:
                sys.stdout.write(f'Not found: {sid}\n')
                sys.exit(1)

    with open(opts.data) as df:
        for line in df:
            did = line.split('\t')[0]
            if did not in data_ids:
                sys.stdout.write(f'Not found: {did}\n')
                sys.exit(1)


if __name__ == '__main__':
    main()
