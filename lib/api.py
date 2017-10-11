#!/usr/bin/env python

import sys
reload(sys)
sys.setdefaultencoding('utf8')

import requests
from pprint import pprint

base_url = 'http://freezone.internode.on.net/api/?'

def none2null(dic):
    dic2 = {}
    for k,v in dic.iteritems():
        if v == None:
            v = ''
        dic2[k] = v
    return dic2

class Media:
    def __init__(self, dic):
        self.dic = dic
        self.bitrate = dic.get('bitrate')
        self.file = dic.get('file')
        self.hls = dic.get('hls')
        self.quality = dic.get('quality')
        self.hls = dic.get('hls')
        self.raw = dic.get('raw')
        print self.dic

    def __repr__(self):
        return "Media %s (%s): %s" % (self.bitrate, self.quality, self.file)

class Video:
    def __init__(self, dic):
        self.dic = dic
        self.description = dic.get('description')
        self.duration = dic.get('duration')
        self.enddate = dic.get('enddate')
        self.icon = dic.get('icon')
        self.id = dic.get('id')
        self.isLive = dic.get('isLive')
        self.likes = dic.get('likes')
        self.media = [Media(m) for m in dic.get('media')]
        self.meta = dic.get('meta')
        self.netconnect = dic.get('netconnect')
        self.num_played = dic.get('num_played')
        self.offset_end = dic.get('offset_end')
        self.offset_start = dic.get('offset_start')
        self.poster = dic.get('poster')
        self.restriction = dic.get('restriction')
        self.smil = dic.get('smil')
        self.startdate = dic.get('startdate')
        self.thumb = dic.get('thumb')
        self.title = dic.get('title')
        print self.dic

    def __repr__(self):
        return "Video %s: %s" % (self.id, self.title.encode('utf-8'))

class Item:
    def __init__(self, dic):
        self.dic = dic = none2null(dic)
        self.description = dic.get('description')
        self.enddate = dic.get('enddate')
        self.icon = dic.get('icon')
        self.id = dic.get('id')
        self.isLive = dic.get('isLive')
        self.likes = dic.get('likes')
        self.link = dic.get('link')
        self.meta = dic.get('meta')
        self.num_played = dic.get('num_played')
        self.order = dic.get('order')
        self.poster = dic.get('poster')
        self.startdate = dic.get('startdate')
        self.thumb = dic.get('thumb')
        self.title = dic.get('title')

    def __repr__(self):
        return "Item %s: %s" % (self.id, self.title.encode('utf-8'))

class Channel:
    def __init__(self, dic):
        self.dic = dic
        self.alias = dic.get('alias')
        self.channels = []
        if dic.has_key('channels'):
            self.channels = [Channel(c) for c in dic['channels']]
        self.description = dic.get('description')
        self.icon = dic.get('icon')
        self.id = dic.get('id')
        self.items = []
        if dic.has_key('items'):
            self.items = [Item(i) for i in dic['items']]
        self.link = dic.get('link')
        self.meta = dic.get('meta')
        self.order = dic.get('order')
        self.thumb = dic.get('thumb')
        self.title = dic.get('title')

    def __repr__(self):
        return u"Channel %s: %s" % (self.id, self.title.encode('utf-8'))

class Category:
    def __init__(self, dic):
        self.dic = dic
        self.banner = dic.get('banner')
        self.description = dic.get('description')
        self.device = dic.get('device')
        self.icon = dic.get('icon')
        self.id = dic.get('id')
        self.image = dic.get('image')
        self.level = dic.get('level')
        self.link = dic.get('link')
        self.order = dic.get('order')
        self.parent = dic.get('parent')
        self.poster = dic.get('poster')
        self.subcats = [Category(c) for c in dic.get('subcats')]
        self.thumb = dic.get('thumb')
        self.title = dic.get('title')

    def __repr__(self):
        return "Category %s: %s" % (self.id, self.title.encode('utf-8'))

class Freezone:

    def __init__(self):
        self.root_channel_json = ''

    def get_navigation(self):
        """
        Get a complete heirarchy of all Categories.
        """
        categories = []
        self.navigation = requests.get(base_url + 'navigation').json()
        for dic in self.navigation:
            category = Category(dic)
            categories.append(category)
        return categories

    def get_channel(self, link):
        """
        Get a Channel.
        """
        return Channel(requests.get(base_url + 'channel=' + link).json())

    def get_root_channels(self):
        """
        Get a list of the Channels at the root level.
        """
        if not self.root_channel_json:
            self.root_channel_json = requests.get(base_url + 'channel=/freezone/').json()
        return [Channel(c) for c in self.root_channel_json.get('channels')]

    def get_root_radio_channels(self):
        """
        Get a list of the radio Channels at the root level.
        """
        root_radio_channel_json = requests.get(base_url + 'channel=/freezone/music/radio/').json()
        return [Channel(c) for c in self.root_channel_json.get('channels')]

    def get_freezone_partners(self):
        """
        Get a list of freezone_partners.
        No Class implemented, returns JSON dict.
        """
        if not self.root_channel_json:
            self.get_root_channels()
        return self.root_channel_json.get('meta').get('freezone_partners').get('partners').get('partner')

    def get_abc_iview(self):
        """
        Get a list of ABC iView videos.
        Just returns a list of links to the ABC iView site. Not directly playable.
        No Class implemented, returns JSON dict.
        """
        return requests.get(base_url + 'abc-iview').json()

    def get_currently_watched(self):
        """
        Get a list of the items currently being watched.
        No Class implemented, returns JSON dict.
        """
        return requests.get(base_url + 'currently-watched').json()

    def get_whats_live(self):
        """
        Get a list of available live items.
        No Class implemented, returns JSON dict.
        Returns more data than get_live.
        """
        return requests.get(base_url + 'whats-live').json()

    def get_live(self):
        """
        Get a list of available live Videos.
        """
        return [Video(v) for v in requests.get(base_url + 'live').json()]

    def get_most_recent(self):
        """
        Get a list of recently added items.
        No Class implemented, returns JSON dict.
        """
        return requests.get(base_url + 'most-recent').json()

    def get_video(self, id):
        """
        Get video media information for playback.
        """
        return Video(requests.get(base_url + 'video=' + str(id)).json())
