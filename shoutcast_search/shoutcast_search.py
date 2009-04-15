#! /usr/bin/env python
#
#   shoutcast_search.py - a library to search shoutcast.com
#
#   Copyright (c) 2009 by Henrik Hallberg (halhen@k2h.se)
#   http://code.k2h.se
#   Please report bugs or feature requests by e-mail. Also, I'd be happy
#   to hear from you if you enjoy this software.
#
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 2 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import urllib
import urllib2
import re
import random
from htmlentitydefs import name2codepoint

def _build_search_url(params):
    '''
    Return URL to search web service with appropriately encoded parameters.
      params - See urllib.urlencode
    '''
    baseurl = 'http://yp.shoutcast.com/sbin/newxml.phtml?'
    params_str = urllib.urlencode(params)
    return baseurl + params_str

def _decode_entities(s):
    '''
    Return string with converted htmlentities, e.g. &auml;
      s - string to convert
    '''
    return re.sub('&(%s);'% ('|'.join(name2codepoint)), lambda(m): chr(name2codepoint[m.group(1)]), s)

def _retrieve_search_results(params):
    '''
    Perform search against shoutcast.com web service.
      params - See urllib.urlencode and http://forums.winamp.com/showthread.php?threadid=295638
    '''
    content = urllib2.urlopen(_build_search_url(params)).read()

    lp = re.compile('<station ')
    p = re.compile(' (.*?)=\"(.*?)\"')
    res = [p.findall(c) for c in content.split('\n') if lp.match(c)]

    def _info_to_dict(row):
        d = {}
        for el in row:
            d[el[0]] = el[1]
        d['name'] = _decode_entities(d['name'])
        d['genre'] = _decode_entities(d['genre'])
        d['ct'] = _decode_entities(d['ct'])
        d['lc'] = int(d['lc'])
        d['br'] = int(d['br'])
        d['id'] = int(d['id'])
        return d
    
    return [_info_to_dict(r) for r in res]        

def url_by_id(index):
    '''
    Returns the stations URL based on its ID
    '''
    return 'http://yp.shoutcast.com/sbin/tunein-station.pls?id=%s' % index

def get_genres():
    '''
    Returns a list of genres (listed by the shoutcast web service).
    Raises urllib2.URLError if network communication fails
    '''
    content = urllib2.urlopen('http://yp.shoutcast.com/sbin/newxml.phtml').read()
    return list(re.compile('<genre name="(.*?)"').findall(content))

def search(search = [], station = [], genre = [], song = [], bitrate_fn = lambda(x): True, listeners_fn = lambda(x): True, mime_type = '', limit = 0, randomize = False, sorters = []):
    '''
    Search shoutcast.com for streams with given criteria. See http://forums.winamp.com/showthread.php?threadid=295638 for details and rules. Raises urllib2.URLError if network communication fails.
      search - List of free-form keywords. Searches in station names, genres and songs.
      station - List of phrases to find in station names.
      genre - List of phrases to find in genres.
      song - List of phrases to find in "currently playing" string - e.g artist or song name.
      bitrate_fn - function with bitrate as argument. Should return True if station is a keeper.
      listeners_fn function with number of listeners as argument. Should return True if station is a keeper.
      mime_type - filter stations by MIME type
      limit - maximum number of stations returned. 0 means unlimited.
      randomize - should results be returned in random order? True / False
      sorters - a list of functions accepting the station list and returning a modified one. Executed after randomization / sorting by number of listeners.

    Returns a list with one dict per station. Each dict contains:
      'name' - station name
      'mt' - mime type
      'id' - station id (used in URL)
      'br' - bitrate in kbps
      'genre' - station genre(s)
      'ct' - currently played track
      'lc' - listener count
    '''

    opt_dict = {}
    keywords = search + station + genre + song

    if mime_type:
        opt_dict['mt'] = mime_type

    if not keywords: # No content to search, use default
        opt_dict['genre'] = 'Top500'

        # Perform search with empty keywords
        results = _retrieve_search_results(opt_dict)
    else:
        # Find everything applicable and filter ourselves, since the API is limited
        # Not very elegant, and quite slow with big queries. No problem with normal use, though.
        results = []
        known_ids = [] # "cache" found station ids to make code easier below
        for k in keywords:
            opt_dict.update({'search': k})
            results += [row for row in _retrieve_search_results(opt_dict) if row['id'] not in known_ids]
            known_ids = [row['id'] for row in results]

    # Filter for bitrate
    results = [r for r in results if bitrate_fn(r['br'])]
    # Filter by listeners
    results = [r for r in results if listeners_fn(r['lc'])]

    # Now filter all the stations we've got. AND all criteria. Not super fast, but OK for normal use
    for s in station:
        results = [r for r in results if s.upper() in r['name'].upper()]
    for g in genre:
        results = [r for r in results if g.upper() in r['genre'].upper()]
    for s in song:
        results = [r for r in results if s.upper() in r['ct'].upper()]
    for k in keywords:
        results = [r for r in results if k.upper() in ('%s %s %s' % (r['name'], r['genre'], r['ct'])).upper()]

    if randomize:
        random.shuffle(results)
    else:
        # Sort by listener count
        results.sort(lambda a, b: cmp(int(a['lc']), int(b['lc'])), reverse=True)

    for m in sorters:
        results = m(results)

    if limit > 0:
        results = results[:limit]

    return results
