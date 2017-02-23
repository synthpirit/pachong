#!/usr/bin/python
#-*- coding: UTF-8 -*-
import time
import os
import print_url_list as pul
import download as dl

url = 'http://mysql.taobao.org/monthly/'
if os.path.exists('url_list.txt'): 
	f = open('url_list.txt','r')
	f_str = f.read()
	f.close()
	url_list = f_str.split('\n')
else:
	url_list = pul.get_url_list(url)
if os.path.exists('downloaded_url_list.txt'):
	f = open('downloaded_url_list.txt')
	downloaded_url_list_str = f.read()
	f.close()
	downloaded_url_list = downloaded_url_list_str.split('\n')
else:
	downloaded_url_list = []

download_url_list = list(set(url_list).difference(set(downloaded_url_list)))
print 'there are'+ str(len(download_url_list)) + ' url to download'
print 'totall '+ str(len(url_list)) + ' urls'
print  str(len(downloaded_url_list))+' urls downloaded'
print downloaded_url_list
time.sleep(3)
#os._exit()
for i,element in enumerate (download_url_list):
	dl.download_data(element)
	print 'downloading' + '  '+str(i+1)+'th url    '+element 
