from google import search
import urllib2
from bs4 import BeautifulSoup
import requests
from subprocess import call
import sys
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


links=[]
counts=[]
final=[]
depth=1
def checkmp3(url):
	if url.endswith(".mp3"):
		return 1
		"""print url,"found. Wanna download"
		ans=raw_input()
		if ans=="Y" or ans=="y":
			download(url)
		final.append(url)
		if len(final) >= 10:
			break
		links.pop(0)              #remove that link
		counts.pop(0)             #remove its count too
		"""
	else:
		return 0


def rectify(links,counts):
	m=zip(links,counts)
	r=((i,j) for (i,j) in m if j < depth)
	return map(list,zip(*r))
def download(url):
	url=url.split(".mp3")[0]+".mp3"
	print "url is ",url
	ans=raw_input()
	if ans=="Y" or ans=="y":
		call(['wget',url])
	return 0


if __name__=='__main__':
	query  = " ".join(sys.argv[1:])
	raw_input(query)
	#websites which should be ignored
	substring_list=["muzmo","wikipedia","youtube","facebook","apple","itunes","firefox","mp3goo","jpeg","images","twitter","soundcloud","blogspot","pinterest","google","goo.gl","shopify","amazon","gaana"]

	#use this to get google search about first 10 websites
	for j in search(query,num=10,stop=10,pause=2):
		links.append(j)
		counts.append(0)
	##rectify links and ignore if above websites are present
	links=[link for link in links if not any(substring in link for substring in substring_list)]
	#print all the genuine links
	
	

	for i in range(len(links)):
		print links[i],counts[i]
	raw_input("enter if these links are okay")
	#while all links are not crawled
	while len(links) > 0:
		url=links[0]
		d=counts[0]

		print "spider ",url,d
		
		#increase depth by 1
		d+=1
		#final.append(links.pop(0))
		links.pop(0)
		counts.pop(0)
		try:
			content=urllib2.urlopen(url,timeout=5).read()
			soup=BeautifulSoup(content)
			for link in soup.find_all('a'):
				l = link.get('href')
				if(checkmp3(l)==1):
					final.append(l)
					continue
				if not any(substring in l for substring in substring_list):
					#links.append(url+l)
					links.append(l)
					counts.append(d)
		except Exception as e:
			print "unable to spider at ",url
			print e
		try:
			links,counts=rectify(links,counts)
		except Exception as e:
			print "error at",url
			print e

	for i in final:
		print i

