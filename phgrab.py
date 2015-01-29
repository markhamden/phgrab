#!/usr/bin/env python3
''' phgrab.py: pornhost.com clip downloader. '''

import os
import sys
import argparse
import urllib.request
import bs4


def reporthook(blocknum, blocksize, totalsize):
    ''' Define the reporthook for url-retrieval
    (displays info while grabbing). '''
    readsofar = blocknum * blocksize
    if totalsize > 0:
        percent = readsofar * 1e2 / totalsize
        display = "\r%*d / %d %5.0f%%" % (
            len(str(totalsize)), readsofar, totalsize, percent)
        sys.stdout.write(display)
        if readsofar >= totalsize:
            sys.stdout.write("\n")
    else:   # total size unknown
        sys.stderr.write("read %d\n" % (readsofar,))


PARSER = argparse.ArgumentParser(
    description="a commandline pornhost.com clip downloader.")
PARSER.add_argument('clipcode', nargs='+',
                    help="a ten-digit pornhost.com clipcode.")
PARSER.add_argument('-p', '--proxy',
                    help="A http proxy to use; e.g. http://localhost:8000")

PROXY = PARSER.parse_args().proxy
CLIPCODES = PARSER.parse_args().clipcode

if PROXY:
    print("Grabbing through http proxy: %s\n" % PROXY)
    os.environ['http_proxy'] = PROXY

for i in CLIPCODES:
    if not i.isdigit() or not len(i) == 10:
        sys.exit(
            "'\033[1m%s\033[0m' is not a valid ten-digit clipcode," % i,
            "please check your input and try again.")

for i in CLIPCODES:
    soup = bs4.BeautifulSoup(
        urllib.request.urlopen("http://pornhost.com/%s" % i))
    title = soup.find("h1", class_="video-title").string
    href = soup.find("a", class_="download button")['href']
    print("Grabbing \033[1m%s\033[0m:" % i)
    local_filename, headers = urllib.request.urlretrieve(
        href, '%s - %s.mp4' % (i, title), reporthook)
    print("\033[1m", local_filename, "Done\033[0m")
