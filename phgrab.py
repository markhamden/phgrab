#!/usr/bin/env python3
''' phgrab.py: pornhost.com clip downloader. v1.1'''

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
        print(display, end='')
    else:   # total size unknown
        print("read %d\n" % (readsofar,), end='')


def main():
    ''' Main method, to be improved at a later date. '''
    print("phgrab.py v1.1; Please consider making a donation: 1A6YkGKYy2bBTN56cad339sW7AxTNpFgch\n")

    parser = argparse.ArgumentParser(
        description="a commandline pornhost.com clip downloader. v1.1")
    parser.add_argument('clipcode', nargs='+',
                        help="a ten-digit pornhost.com clipcode.")
    parser.add_argument('-p', '--proxy',
                        help="A http proxy to use; e.g. http://localhost:8000")

    proxy = parser.parse_args().proxy
    clipcodes = parser.parse_args().clipcode

    if proxy:
        print("Grabbing through http proxy: %s\n" % proxy)
        os.environ['http_proxy'] = proxy

    for clipcode in clipcodes:
        if not clipcode.isdigit() or len(clipcode) != 10:
            print(
                "'\033[1m%s\033[0m' is not a valid ten-digit clipcode, please check your input and try again." % clipcode)
            sys.exit(1)

    for clipcode in clipcodes:
        soup = bs4.BeautifulSoup(
            urllib.request.urlopen("http://pornhost.com/%s" % clipcode))
        title = soup.find("h1", class_="video-title").string
        href = soup.find("a", class_="download button")['href']
        print("Grabbing \033[1m%s - %s.mp4\033[0m:" % (clipcode, title))
        local_filename, headers = urllib.request.urlretrieve(
            href, '%s - %s.mp4' % (clipcode, title), reporthook)
        print("\033[1m Done\033[0m\n")

if __name__ == "__main__":
    main()
