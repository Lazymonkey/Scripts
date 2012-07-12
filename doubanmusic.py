#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import urllib, urllib2, cookielib, re, json, eyeD3, os

num_p = re.compile(r'(\d+)')
songs_dir = 'songs'
base_url = 'http://douban.fm/j/mine/playlist?type=n&h=&channel=0&context=channel:0|subject_id:%s'

def get_songs_information(url):
    subject_id = num_p.search(url).groups()[0]
    ret = json.loads(urllib2.urlopen(base_url % subject_id).read())
    return filter(lambda x:x['album'].endswith(subject_id+'/'), ret['song'])

def download(song):
    try:
        os.mkdir(songs_dir)
    except:
        pass
    filename = '%s.mp3' % song['title']
    filepath = os.path.join(songs_dir, filename)
    if os.path.exists(filepath):
        return
    urllib.urlretrieve(song['url'], filepath)
    picname = song['picture'][1+song['picture'].rindex('/'):]
    picpath = os.path.join(songs_dir, picname)
    urllib.urlretrieve(song['picture'], picpath)
    tag = eyeD3.Tag()
    tag.link(filepath)
    tag.header.setVersion(eyeD3.ID3_V2_3)
    tag.encoding = '\x01'
    tag.setTitle(song['title'])
    tag.setAlbum(song['albumtitle'])
    tag.setArtist(song['artist'])
    tag.setDate(song['public_time'])
    tag.addImage(3, picpath)
    os.remove(picpath)
    tag.update()

def html_decode(html):
    #return html.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '"').replace('&#39;', "'")
    import HTMLParser
    return HTMLParser.HTMLParser().unescape(html)

def get(myurl, cookie):
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookielib.CookieJar()))
    urllib2.install_opener(opener)
    req = urllib2.Request(myurl)
    req.add_header('User-Agent', 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)')
    req.add_header('Cookie', cookie)
    content = urllib2.urlopen(req).read()
    soup = BeautifulSoup(str(content))
    for div in soup.findAll('div', {'class' : 'info_wrapper'}):
        p = div.find('div', {'class' : 'song_info'}).findAll("p")
        sid = div.find('div', {'class' : 'action'})['sid']
        print "song:" + html_decode(p[0].string) + "\nsinger:" + html_decode(p[1].string) + "\nalbum:" + html_decode(p[2].a.string)
        mark = False
        try:
            for j in range(10):
                songs = get_songs_information(str(p[2].a))
                for song in songs:
                    if sid == song['sid']:
                        print song['url']
                        download(song)
                        mark = True
                        break
                if mark:
                    break
            if mark:
                print 'succeed!\n\n'
            else: print 'fail!\n\n'
        except Exception as e:
            print e.message+'\n'

def main():
    url = 'http://douban.fm/mine?start=%d&type=liked'
    #cookie = raw_input('cookie:')
    cookie = 'bid="OiUSmsw9v8o"; __gads=ID=90a217c6afbfb8f8:T=1336221096:S=ALNI_MYbgGtfZq8YI6NAqRqH-xxEJuTGog; dbcl2="53653304:UaI4O5wiQdE"; ct=y; ll="118323"; ck="nL_C"; __utma=30149280.1459427903.1338015263.1338015263.1338015549.2; __utmb=30149280.9.9.1338015887569; __utmc=30149280; __utmz=30149280.1338015549.2.5.utmcsr=bing|utmccn=(organic)|utmcmd=organic|utmctr=%E8%B1%86%E7%93%A3%20%E6%95%B0%E6%8D%AE%E6%8C%96%E6%8E%98; __utmv=30149280.5365'
    print 'you should enter the pages you want to download'
    page0 = int(raw_input('page from:'))
    page1 = int(raw_input('page to:'))
    for i in range(page1-page0+1):
        get(url%((i+page0-1)*15), cookie)

if __name__ == '__main__':
    main()
