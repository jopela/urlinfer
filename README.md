# urlinfer 

takes a list of url (e.g: http://en.wiki.org/w/russia, http://en.wiki.org/can)
and apply monoid functions on the list in order to produce a new list with
new addresses, or addresses modified.

## example

The goal is to 'guess' the url of other resources based on some already
existing resources. This is made clear by the following example:

```bash
urlfinder.py http://en.wiki.org/wiki/Montreal http://ru.db.org/res/Russia
-i wikivoyage languages
```

which should return:

```bash
http://en.wiki.org/wiki/Montreal http://en.voyage/wiki/Montreal  
http://ru.wiki.org/wiki/Russia http://ru.voyage/wiki/Russia
```
the arguments given to -i must be a list of existing monoid function which
are simply composed. The application order is from right to left, meaning
that for the example above, the result is given by 
(wikivoyage((languages(list))).



