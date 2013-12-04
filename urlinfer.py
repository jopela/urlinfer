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
            nargs='+'
            )

    parser.add_argument(
            '-t',
            '--test',
            help='run the test suit and exit',
            action='store_true',
            default=False
            )

    args = parser.parse_args()

    if args.test:
        import doctest
        doctest.testmod()
        exit(0)

    urls = args.urls.read().split()
    functions = args.inferfunc

    return

def wikivoyage(urls):
    """ takes a list of urls and infers the wikivoyage urls from them.

    Example
    =======

    # empty list should returnt the empty list.
    >>> wikivoyage([])
    []

    # wikipedia urls should be 'casted' to wikivoyage urls.
    >>> wikivoyage(['http://en.wikipedia.org/wiki/Montreal'])
    ['http://en.wikipedia.org/wiki/Montreal','http://en.wikivoyage.org/wiki/Montreal']

    # non wikipedia urls remain untouched.
    >>> wikivoyage(['http://db.org/resource/Montreal'])
    ['http://db.org/resource/Montreal']
    """

    return []


if __name__ == '__main__':
    main()
