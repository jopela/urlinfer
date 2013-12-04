#!/usr/bin/env python3

import functional
import argparse
import sys

def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
            'urls',
            help='the file containing the list of url to transform. Default'\
            ' to stdin if no file is given',
            nargs='?',
            type=argparse.FileType('r'),
            default=sys.stdin
            )

    parser.add_argument(
            '-i',
            '--inferfunc',
            help='inference functions to apply',
            choices = ('wikivoyage', 'language'),
            nargs='+',
            required=True
            )

    args = parser.parse_args()

    urls = args.urls.read().split()
    functions = args.inferfunc


    print("urls: {0}".format(urls))
    print("functions: {0}".format(functions))

if __name__ == '__main__':
    main()
