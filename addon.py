import sys
import urllib
import urlparse
import xbmcgui
import xbmcplugin

from lib import api
    
def build_url(query):
    base_url = sys.argv[0]
    return base_url + '?' + urllib.urlencode(query)

def main():
    args = urlparse.parse_qs(sys.argv[2][1:])
    mode = args.get('mode', None)
    fz = api.Freezone()
    
    # initial launch of add-on
    if mode is None:
        for channel in fz.get_root_channels():
            print "Channel %s %s" % (channel.title, channel.link)
            url = build_url({'mode': 'folder', 'foldername': channel.title, 'link': channel.link})
            li = xbmcgui.ListItem(channel.title, channel.thumb)
            xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)
        xbmcplugin.endOfDirectory(addon_handle)

    # a folder has been selected
    elif mode[0] == 'folder':
        foldername = args['foldername'][0]
        link = args['link'][0]
        print "Selected folder %s %s" % (foldername, link)
        this_channel = fz.get_channel(link)
        for channel in this_channel.channels:
            print "Channel %s %s" % (channel.title, channel.link)
            url = build_url({'mode': 'folder', 'foldername': channel.title, 'link': channel.link})
            li = xbmcgui.ListItem(channel.title, iconImage=channel.thumb)
            xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)
        for item in this_channel.items:
            print "Item %s %s" % (item.title, item.id)
            video = fz.get_video(item.id)
            url = video.media[-1].hls#raw
            li = xbmcgui.ListItem(video.title, iconImage=video.thumb)
            xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)
            xbmcplugin.endOfDirectory(addon_handle)
        xbmcplugin.endOfDirectory(addon_handle)

    # a station from the list has been selected
    elif mode[0] == 'stream':
        print "Playing video stream '%s' %s" % (args['title'][0], args['url'][0])
        pass
    
if __name__ == '__main__':
    addon_handle = int(sys.argv[1])
    main()
