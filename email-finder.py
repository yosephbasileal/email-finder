# A program that will take an internet domain name and print out a list of the email addresses that were found on that website
# Author: Basileal Imana

import re
from bs4 import BeautifulSoup
import urlparse
import Queue
import argparse

import dryscrape



# Attemps to connect to a webpage and download html
def get_file(url):
	try:
		session = dryscrape.Session()
		session.visit(url)
		response = session.body()
		return response
	except:
		return ""
		
# Gets all email addresses in a html string, returns a set to remove duplicates
def get_emails(html):
	email_re = r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+"
	emails = re.findall(re.compile(email_re), html)
	return set(emails)

# Gets all links in an html string that link to a page within the given domain
def get_links(html, base_url):
	links = set() # use a set to avoid duplicates
	s = BeautifulSoup(html, "html.parser")
	a = s.find_all('a')
	# for each 'a' html element found
	for link in a:
		# get link address
		l = link.get('href')

		# combine relative path with base_url
		new_url = urlparse.urljoin(base_url, l)

		# parse the full url
		o = urlparse.urlparse(new_url)

		# parse base_url to get domain
		d = urlparse.urlparse(base_url)

		# add only if from the same domain
		if(o.netloc == d.netloc):
			links.add(o.geturl())

	return links

# Parses command line arguments
def arg_parser():
	parser = argparse.ArgumentParser(
		description="Crawls a webstie and look for email addresses")
	parser.add_argument('domain_name', 
		help = "Website to be crawled")
	parser.add_argument('-d',
		help = "Maximum page tree depth to reach",action="store", default=1)
	parser.add_argument('-o',
		help = "Output url being crawled for debugging purpose", action="store_true", default=False)
	return parser.parse_args()


# Main runner function
def run():
	# get arguments
	args = arg_parser()
	base_url = "http://" + args.domain_name
	depth_max = int(args.d)
	output = args.o

	# initializes queue and set of emails and links
	q = Queue.Queue()
	all_links = set()
	all_emails = set()

	# start crawling from base_url
	q.put((base_url, 0)) # queue stores a (link, depth) tuple
	all_links.add(base_url)
	
	# while there are remaining pages to crawl
	while not q.empty():

		# pop next link from queue
		url_t = q.get() # get (link, depth) tuple
		url = url_t[0] # get url
		depth = url_t[1] # get current depth

		# output for debugging
		if(output):
			print "(" + str(depth) + ")" + url

		# get html string of current page
		html = get_file(url)
		
		# extract emails addresses
		emails = get_emails(html)

		# find href links
		links = get_links(html, base_url)

		# for each link found
		for link in links:
			# check if not already visited and if depth doesnt exceed max-depth
			if link not in all_links and depth <= depth_max:
				# add to queue, increment depth
				q.put((link, depth + 1))

		# update set
		all_emails.update(emails)
		all_links.update(links)

	# output emails, if any
	for e in all_emails:
		print e

run()
	
	


