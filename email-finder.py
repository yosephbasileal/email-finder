import re, urllib
from bs4 import BeautifulSoup
import Queue

# Attemps to connect to a webpage and download html
def get_file(url):
	try:
		html_file = urllib.urlopen(url)
		html = html_file.read()
		return html
	except IOError:
		print "Unable to make connection. Try again..."
		
# Gets all email addresses in a html string, returns a set to remove duplicates
def get_emails(html):
	email_re = r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+"
	emails = re.findall(re.compile(email_re), html)
	return set(emails)

def get_links(html, base_url):
	s = BeautifulSoup(html, "html.parser")
	a = s.find_all('a')
	for link in a:
		l = link.get('href')
		# print l

# Main runner function
def run():
	# get url
	base_url = "http://old-www.jana.com/"

	# initializes queue of links and set of emails
	q = Queue.Queue()
	all_links = set()
	all_emails = set()
	q.put(base_url)
	
	# while there are remaining pages to crawl
	while not q.empty():
		# get html string of current page
		url = q.get()
		html = get_file(url)
		
		# extract emails addresses and update set
		emails = get_emails(html)

		# find href links and add to queue
		# links = get_links(html, base_url)

	# output emails, if any
	for e in all_emails:
		print e

run()
	
	


