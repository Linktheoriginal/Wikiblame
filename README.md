# Wikiblame
Django Blamer for Mediawiki APIs

Quick Django app to use the simplemediawiki Python Library to access a wiki page and linearly search the page versions for a given string.

Created because hunting through page versions for who added a given line was annoying.

This is designed to login to private wikis (designed to be used on an internal wiki).

Simple implementation maxes out at 5000 requests - and large pages can run it out of memory.
