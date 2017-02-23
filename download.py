#!/usr/bin/python
#-*- coding: UTF-8 -*-
from pyquery import PyQuery as pq
import os
import urllib2
import re

def download_data(url):
	try:
		print 'opening '+url	
		doc = pq(url)
		print 'done'
	except urllib2.URLError, e:
		print e.reason
		#return
		
	html_title = doc('title').html()        #unicode
	web_root = doc.base_url.split('//')[0] + '//' + doc.base_url.split('//')[1].split('/')[0]
	try:  
		folder_name = html_title.encode('gbk') + '_files'
	except UnicodeEncodeError :
		print 'gbk encode error'
		return url
	folder_path = os.getcwd()+'/'+folder_name
	try:
		os.mkdir(folder_path)
	except OSError, e:
		print 'oserror ,not know now skip...'
		return url
	
	  
	stylesheet_link_tag = doc('link[rel=stylesheet]')
	for i in stylesheet_link_tag:
	    link_href = i.get('href')        
	    if link_href.find('//') == -1:
	        stylesheet_link_tag_href_url = web_root + link_href
	    elif link_href.find('//') == 0:
	        stylesheet_link_tag_href_url = 'http:' + link_href
	    else:
		stylesheet_link_tag_href_url = link_href
	    try:
		print 'opening '+stylesheet_link_tag_href_url
		response = urllib2.urlopen(stylesheet_link_tag_href_url)   
		print 'done'
	    except urllib2.URLError, e:
		print e.reason
	    css = response.read()
	    file_name = link_href.split('//')[-1].split('/')[-1]
	    file_name = re.sub(r'[\\/*:<>?|"]','_',file_name) # comptiable file_names for windows
	    file_path = folder_path+'/'+file_name
	    f = open(file_path,'w')
	    f.writelines(css)
	    file_path_u = u'./' + html_title + u'_files/' + file_name.decode()
	    i.set('href',file_path_u)                #file_path带修改
	
	script_tag = doc('script[src],img[src]')	
	for i in script_tag:	
	    src = i.get('src')
	    if src.find('//') == -1:
	        src_url = web_root + src
	    elif src.find('//') == 0:
	       	src_url = 'http:' + src
	    else:
		if src.find('creativecommons.org') != -1:
			continue
		else:
			src_url = src
	    try:		
		print 'opening '+src_url
		response = urllib2.urlopen(src_url)
		print 'done'
	    except urllib2.URLError, e:
		print e.reason
	    js = response.read()
	    file_name = src.split('//')[-1].split('/')[-1]
	    file_name = re.sub(r'[\\/*:<>?|"]','_',file_name) # comptiable file_names for windows
	    file_path = folder_path+'/'+file_name
	    file_path = folder_path+'/'+file_name
	    f = open(file_path,'w')
	    f.writelines(js)
	    file_path_u = u'./' + html_title + u'_files/' + file_name.decode()
	    i.set('src',file_path_u)				 #file_path带修改
	html_file_name = html_title.encode('gbk') + '.html'              #write html to folder
	html_file_path = os.getcwd() + '/' + html_file_name
	html_file = open(html_file_path,'w')
	html_u = doc.html()    #unicode
	html = html_u.encode('utf8')
	html_file.writelines(html)
	html_file.close()
	downloaded_url_list = open('downloaded_url_list.txt','a')
	downloaded_url_list.write(url+'\n')
	downloaded_url_list.close()	
	return
if __name__ =='__main__':
	import sys
	url = sys.argv[1]
	print url
	download_data(url)
