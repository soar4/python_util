#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#   Author  :   gaofei
#   Date    :   18/2/15 17:16:21
#   Desc    :

from BeautifulSoup import BeautifulSoup
import sys
import re
import urllib2
import base64

baseFilter = [r'^thunder://', r'^ftp://', r'^ed2k://', r'^magnet:']
g_dl_html = './dl.html'

def download(url):
	try:
		request = urllib2.Request(url)
		resp = urllib2.urlopen(request)
	except Exception as e:
		print 'url open failed.[{}]'.format(url)
		return None
	body = resp.read()
	return body

def dump(content, fpath):
	f = open(fpath, 'wb')
	f.write(content)

def load(fpath):
	f = open(fpath, 'rb')
	content = f.read()
	return content


def urls(soup, content):
	links = []
	for tags in soup.findAll(href=True):
		bmatched = False
		link = tags['href']
		for reg in baseFilter:
			# print 'type:%s,val:%s;type:%s,val:%s' % (type(reg), reg, type(link), link)
			if re.match(reg, link):
				bmatched = True
				break
		if not bmatched:
			continue
		if link not in links:
			links.append(link)
	return links


def decode_thunder(thunder_url):
	b64 = thunder_url[12:len(thunder_url)-2]
	print "org:", thunder_url
	print "b64:", b64
	deb64 = base64.b64decode(b64)
	return deb64

def url_to_body(url):
	body = download(url)
	if not body:
		sys.exit(1)
	fpath = g_dl_html
	dump(body, fpath)
	return body

def main(url,bQuick):
	content = None
	if bQuick:
		content = load(g_dl_html)
	else:
		content = url_to_body(url)
	soup = BeautifulSoup(content)
	links = urls(soup, content)
	for link in links:
		print link
		# if re.match(r'^thunder://', link):
		# 	print decode_thunder(link)
		# break
	print 'total link num:', len(links)


if __name__ == '__main__':
	if len(sys.argv) < 2:
		print "usage:{} url".format(sys.argv[0])
		sys.exit(0)
	url = sys.argv[1]
	bQuick = False
	if len(sys.argv) > 2:
		bQuick = True
	main(url, bQuick)

