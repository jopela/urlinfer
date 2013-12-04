#!/usr/bin/env python3

import functional
import argparse
import sys

from urllib.parse import urlparse, urlunparse

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
            choices = ('wikivoyage', 'dbpedia'),
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

    # empty list should return the empty list.
    >>> wikivoyage([])
    []

    # wikipedia urls should be 'casted' to wikivoyage urls.
    >>> wikivoyage(['http://en.wikipedia.org/wiki/Montreal'])
    ['http://en.wikipedia.org/wiki/Montreal', 'http://en.wikivoyage.org/wiki/Montreal']

    # non wikipedia urls remain untouched.
    >>> wikivoyage(['http://db.org/resource/Montreal'])
    ['http://db.org/resource/Montreal']

    # wikipedia should only be replace in the netloc
    >>> wikivoyage(['http://en.wikipedia.org/wiki/wikipedia'])
    ['http://en.wikipedia.org/wiki/wikipedia', 'http://en.wikivoyage.org/wiki/wikipedia']

    """
    res = []
    wikipedia_domain = "wikipedia"
    wikivoyage_domain = "wikivoyage"

    for url in urls:
        res.append(url)
        parsed = urlparse(url)
        if wikipedia_domain in parsed.netloc:
            wikivoyage_url = urlunparse(
                    (parsed.scheme,
                     parsed.netloc.replace(wikipedia_domain, wikivoyage_domain),
                     parsed.path,
                     parsed.params,
                     parsed.query,
                     parsed.fragment)
                    )
            res.append(wikivoyage_url)

    return res

def dbpedia(urls):
    """ takes a list of urls and transform the dbpedia urls into
    wikipedia urls.

    Example
    =======

    # empty list should return the empty list.
    >>> dbpedia([])
    []

    # dbpedia urls should be casted to wiki urls.
    >>> dbpedia(['http://ru.dbpedia.org/resource/Россия'])
    ['http://ru.wikipedia.org/wiki/Россия']

    # non dbpedia urls remain untouched.
    >>> dbpedia(['http://en.wikipedia.org/wiki/S-expression'])
    ['http://en.wikipedia.org/wiki/S-expression']

    """

    res = []
    dbpedia_domain = "dbpedia"

    return []


if __name__ == '__main__':
    main()
