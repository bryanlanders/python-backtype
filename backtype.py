#!/usr/bin/env python
#
# Copyright 2009 Bryan Landers
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

"""A Python wrapper for the BackType API v1

API documentation is available at http://www.backtype.com/developers.

Example code:
import backtype_api
api = backtype_api.BackType(api_key='[YOUR_API_KEY]')
comments_connect_stats = api.comments_connect_stats('http://blog.backtype.com/2009/03/backtweets-search-links-on-twitter/')
comments_connect = api.comments_connect(url='http://blog.backtype.com/2009/03/backtweets-search-links-on-twitter/')
comments_search = api.comments_search('backtype')
url_comments = api.url_comments('http://blog.backtype.com')
page_comments = api.page_comments('http://blog.backtype.com/2008/10/backtype-on-friendfeed/')
api.user_profile('backtype')
"""

import datetime
import time
import urllib
import urllib2

# Find a JSON parser
try:
    import simplejson
    _parse_json = lambda s: simplejson.loads(s.decode("utf-8"))
except ImportError:
    try:
        import cjson
        _parse_json = lambda s: cjson.decode(s.decode("utf-8"), True)
    except ImportError:
        try:
            import json
            _parse_json = lambda s: _unicodify(json.read(s))
        except ImportError:
            # For Google AppEngine
            from django.utils import simplejson
            _parse_json = lambda s: simplejson.loads(s.decode("utf-8"))

_BACKTYPE_API_BASE = "http://api.backtype.com"
_BACKTYPE_IMAGE_BASE = "http://www.backtype.com/go/image/p/"


class BackType(object):
    def __init__(self, api_key=None):
        """Initializes a Backtype API wrapper instance.
        """
        self.api_key = api_key


    def comments_search(self, q, **args):
        """Retrieve all conversations related to a given URL.
        
        Arguments:
        q - required; The query string you want to search comments for; supports AND OR NOT and advanced expressions.
        start - Search for comments made after this date YYYY/MM/DD.
        end - Search for comments made before this date YYYY/MM/DD.
        
        See http://www.backtype.com/developers/comments-search.
        """
        return self.fetch("/comments/search.json", q=q, **args)


    def comments_connect(self, url, **args):
        """Retrieve all conversations related to a given URL.
        
        Arguments:
        url - required; The URL you want related conversations for.
        
        See http://www.backtype.com/developers/comments-connect.
        """
        return self.fetch("/comments/connect.json", url=url, **args)
    
    
    def comments_connect_stats(self, url, **args):
        """Retrieve statistics on the conversations related to a given URL.
        
        Arguments:
        url - required; The URL you want related conversations for.
        sources - default = all; Comma delimited list of source titles (native, blog, digg, reddit, yc, friendfeed, twitter) or blog IDs.
        sort - If set to 1, results will be ordered by the date they were found by BackType.
        
        See http://www.backtype.com/developers/comments-connect-stats.
        """
        return self.fetch("/comments/connect/stats.json", url=url, **args)
    
    
    def url_comments(self, url, **args):
        """Retrieve comments written by a particular author.
        
        Arguments:
        url - required; The URL belonging to the blog author you want to retrieve comments for.
        
        See http://www.backtype.com/developers/url-comments.
        """
        return self.fetch("/url/" + url + "/comments.json", **args)
    
    
    def page_comments(self, url, **args):
        """Retrieve excerpts of comments published on a particular page.
        
        Arguments:
        url - required; The post url to return comments for.
        
        See http://www.backtype.com/developers/page-comments.
        """
        return self.fetch("/post/comments.json", url=url, **args)
    
    
    def page_comments_stats(self, url, **args):
        """Retrieve statistics for the comments published on a particular page.
        
        Arguments:
        url - required; The post url to return stats for.
        
        See http://www.backtype.com/developers/page-comments-stats.
        """
        return self.fetch("/post/stats.json", url=url, **args)
    
    
    def user_comments(self, user, **args):
        """Retrieve comments claimed by a BackType user.
        
        Arguments:
        user - required; The BackType username you want to retrieve comments by.
        
        See http://www.backtype.com/developers/user-comments.
        """
        return self.fetch("/user/" + user + "/comments.json", **args)
    
    
    def user_followers(self, user, **args):
        """Retrieve a list of users following a particular BackType user.
        
        Arguments:
        user - required; The BackType username you want to retrieve followers for.
        
        See http://www.backtype.com/developers/user-followers.
        """
        return self.fetch("/user/" + user + "/followers.json", **args)
    
    
    def user_following(self, user, **args):
        """Retrieve a list of users being followed by a particular BackType user.
        
        Arguments:
        user - required; The BackType username you want to retrieve followed users for.
        
        See http://www.backtype.com/developers/user-following.
        """
        return self.fetch("/user/" + user + "/following.json", **args)
    
    
    def user_home_feed(self, user, **args):
        """Retrieve comments written by authors followed by a BackType user.
        
        Arguments:
        user - required; The BackType username you want to retrieve home feed comments for.
        
        See http://www.backtype.com/developers/user-home-feed.
        """
        return self.fetch("/user/" + user + "/home/comments.json", **args)
    
    
    def user_profile(self, user, **args):
        """Retrieve a BackType user's profile information.
        
        Arguments:
        user - required; The BackType username you want to retrieve profile information for.
        
        See http://www.backtype.com/developers/user-profile.
        """
        return self.fetch("/user/" + user + "/profile.json", **args)


    def fetch(self, path, **args):
        """Fetches the given relative API path and returns the response as JSON.
        """
        url = _BACKTYPE_API_BASE + path + "?key=" +  self.api_key
        if args: url += "&" + urllib.urlencode(args)
        request = urllib2.Request(url)
        stream = urllib2.urlopen(request)
        data = stream.read()
        stream.close()
        return data
    
    def fetch_image_url(self, image_id, image_size='t'):
        """Get the URL for a BackType image.
        
        Arguments:
        image_id - required; The BackType image id you want to get a URL for.
        image_size - options: {m,t,p,o}; default = t; The size of the image you want to get a URL for.
        
        See http://www.backtype.com/developers.
        """
        return _BACKTYPE_IMAGE_BASE + image_size + "/" + image_id + ".jpg"
