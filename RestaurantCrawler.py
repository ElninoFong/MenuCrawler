from bs4 import BeautifulSoup
import urllib2
import sys, os

def getLink(currentPage):

	site = ('http://jinshisong.com/zh-CN/restaurants?page=%s') % currentPage
	hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'}
	req = urllib2.Request(site, headers=hdr)

	try:
		page = urllib2.urlopen(req)
	
		result = set()
		soup = BeautifulSoup(page)

		res = soup.find_all(id = 'restaurants-list')
		res = res[0].find_all('a')
		for link in res:
			result.add('http://jinshisong.com/' + link.get('href'))
		return result

	except urllib2.HTTPError, e:
		print e.fp.read()

if __name__ == '__main__':
	try:
		f = open('Links.txt', 'w+')
		links = set()
		for i in range(1, 21):
			links.update(getLink(i))
			print "get %s pages." % i
		for link in links:
			f.write(link + '\n')
		f.close()
	except IOError, e:
		print e


