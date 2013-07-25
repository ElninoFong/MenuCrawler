# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import urllib2
import re
import csv
import codecs, cStringIO

def getMenu(src_file, des_file):
	hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'}

	try:
		links_file = open(src_file, 'r')
		links = []
		for link in links_file:
			links.append(link.replace('\n', ''))
		links_file.close()

		# f = codecs.open(des_file, 'w', encoding="utf-8")
		f = open(des_file, 'w')
		writer = UnicodeWriter(f)
		# writer.writerows(someiterable)

		# print links

		for link in links:
			try:
				req = urllib2.Request(link, headers=hdr)
				page = urllib2.urlopen(req)
			except urllib2.HTTPError, e:
				print e.fp.read()
				continue

			soup = BeautifulSoup(page,from_encoding='utf-8')
			# print soup

			restaurant = soup.find(class_='name').string
			tags = soup.find_all(attrs={"items-count": re.compile(r"\d")})

			for tag in tags:
				try:
					category = tag.find(id=re.compile(r'title-\d')).string
					name = tag.find_all(class_='name')
					price = tag.find_all(text=re.compile(ur'￥\d'))
					for i in range(len(name)):
						try:
							# Get rid of the '￥' sign
							writer.writerow([restaurant, category, name[i].string, price[i].string[1:]])
						except Exception, e:
							print e
							continue
				except Exception, e:
					print e
					continue
			print "finished: " + link

		f.close()

	except IOError, e:
		print e
	



class UnicodeWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([s.encode("utf-8") for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)

getMenu(u"Links_金融街top30.txt", u"Menu_金融街top30.csv")
