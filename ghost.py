#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Hamlet's Ghost, a tool for making sense of spotify urls

version 0.0.1
(c) marcos ojeda, 2013, marcos at generic dot cx
"""
import discogs_client as discogs
import re
import requests
import sys

discogs.user_agent = 'spotty/0.1 +http://generic.cx/'
BASE_URI = 'http://ws.spotify.com/lookup/1/.json'

def query_link(link):
    """ask spotify about one of their urls"""
    payload = {'uri': link}
    data = requests.get(BASE_URI, params=payload)
    if data.status_code == 200:
        data = data.json()
        if data['info']['type'] == 'track':
            d = data['track']
            name = d['name'].lower()
            artist = d['artists'][0]['name'].lower()
            album = d['album']['name'].lower()
            year = d['album']['released']  # this is dodgy
            album, artist, year = corroborate(album, artist, year)
            print '%s, %s (%s)' % (name, artist, year)
        if data['info']['type'] == 'album':
            d = data['album']
            name = d['name'].lower()
            artist = d['artist'].lower()
            year = d['released']
            name, artist, year = corroborate(name, artist, year)
            print '%s, %s (%s)' % (name, artist, year)
        print "  %s" % link
        return
    else:
        sys.stderr.write('[%s] %s' % (data.status_code, data.text.strip()))

def corroborate(name, artist, year):
    """corroborate spotify's dodgy info with discogs"""
    res = discogs.Search("%s, %s" % (name, artist))
    try:
        if res.results()[0]:
            if int(year) != int(res.results()[0].data['year']):
                year = res.results()[0].data['year']
    except Exception:
        pass
    finally:
        return name, artist, year


if __name__ == '__main__':

    rematch = re.compile(r'(http://open\.spotify.com/[ta].*?/.+)[\s\b]?')

    for line in sys.stdin:
        res = rematch.search(line)
        if res:
            query_link(res.group(1))
