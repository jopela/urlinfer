#!/usr/bin/env python3

import argparse
import sys
import functools

from urllib.parse import urlparse, urlunparse
from functional import compose, partial

multi_compose = partial(functools.reduce, compose)

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
            '-l',
            '--lang',
            help='language prefix to use when infering from dbpedia resources'\
                    '. Defaults to "en" when not specified.',
            default = "en"
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

    # turn the function name into function.
    real_functions = [getattr(sys.modules[__name__], name) for name in functions]

    res = infer(urls, real_functions)
    for url in res:
        print(url)
    return

def infer(urls, functions):
    """ takes a list of urls and apply the inference functions on them.

    Example
    =======

    # composition of the dbpedia infer and wikivoyage infer
    >>> infer(['http://ru.dbpedia.org/resource/russia','http://en.wikipedia.org/wiki/quebec'],[wikivoyage,dbpedia])
    ['http://ru.wikipedia.org/wiki/russia', 'http://ru.wikivoyage.org/wiki/russia', 'http://en.wikipedia.org/wiki/quebec', 'http://en.wikivoyage.org/wiki/quebec']
    """

    composed = multi_compose(functions)
    res = composed(urls)

    return res

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

def dbpedia(urls,lang='en'):
    """ takes a list of urls and transform the dbpedia urls into
    wikipedia urls with the given language prefix.

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

    # domain and path should only be replaced at the right position.
    >>> dbpedia(['http://en.dbpedia.org/resource/resource'])
    ['http://en.wikipedia.org/wiki/resource']

    # dbpedia resource with no language prefix in the url domain name must
    # be translated into the default lang (en).
    >>> dbpedia(['http://dbpedia.org/resource/Montreal'])
    ['http://en.wikipedia.org/wiki/Montreal']

    """
    res = []
    dbpedia_domain = "dbpedia"
    wikipedia_domain ="wikipedia"

    def switch_domain(parsed):
        new_netloc = parsed.netloc.replace(dbpedia_domain, wikipedia_domain)
        path = parsed.path.split('/')
        path[1] = 'wiki'
        new_path = '/'.join(path)

        new_url = urlunparse(
                (parsed.scheme,
                 new_netloc,
                 new_path,
                 parsed.params,
                 parsed.query,
                 parsed.fragment)
                )

        return new_url

    urls = [assign_lang(url,lang) for url in urls]

    for url in urls:
        parsed = urlparse(url)
        domain = parsed.netloc

        if dbpedia_domain in domain:
            res.append(switch_domain(parsed))
        else:
            res.append(url)

    return res

def assign_lang(url,lang):
    """ assign a language to a dbpedia resource that does not have one.

    EXAMPLE
    =======

    >>> assign_lang('http://dbpedia.org/resource/Montreal','en')
    'http://en.dbpedia.org/resource/Montreal'

    >>> assign_lang('http://fr.dbpedia.org/resource/Montreal','en')
    'http://fr.dbpedia.org/resource/Montreal'
    """

    url_parsed = urlparse(url)

    domain = url_parsed.netloc
    domain_parts = domain.split(".")

    if len(domain_parts) == 3:
        return url
    else:
        new_netloc = ".".join([lang,domain])
        new_url    = urlunparse(
                       (url_parsed.scheme,
                        new_netloc,
                        url_parsed.path,
                        url_parsed.params,
                        url_parsed.query,
                        url_parsed.fragment))

        return new_url

if __name__ == '__main__':
    main()
