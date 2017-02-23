#!/usr/bin/python
#-*- coding: UTF-8 -*-
from pyquery import PyQuery as pq
import os

def get_url_list(url):
	url_list = []
	print 'downloading '+url
	doc_main = pq(url)
	print 'done'
	web_root = doc_main.base_url.split('//')[0] + '//' + doc_main.base_url.split('//')[1].split('/')[0]
	doc_class_main = doc_main('.main')
	print 'searching urls....'
	for i in doc_class_main:
		main_href = i.get('href')
		if main_href.find('monthly') == -1:
			url_list.append(main_href)
		else:
			sub_url = web_root + main_href
			doc_sub = pq(sub_url)
			doc_sub_small_next = doc_sub('small').next()
			for i in doc_sub_small_next:
				url = web_root + i.get('href')
				url_list.append(url)
	print 'url_list completed,'+str(len(url_list))+'urls in the list'
	f = open('url_list.txt','w')
	for i in url_list:
		f.write(i+'\n')
	f.close()
	return url_list

if __name__ == '__main__':
	import sys
	url = sys.argv[1]
	url_list = get_url_list(url)
	for i in url_list:
		print i
