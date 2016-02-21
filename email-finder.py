import re, urllib
from bs4 import BeautifulSoup
import urlparse
import Queue

# Attemps to connect to a webpage and download html
def get_file(url):
	try:
		html_file = urllib.urlopen(url)
		html = html_file.read()
		return html
	except IOError:
		print "Unable to make connection. Try again..."
		quit()
		
# Gets all email addresses in a html string, returns a set to remove duplicates
def get_emails(html):
	email_re = r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+"
	emails = re.findall(re.compile(email_re), html)
	return set(emails)

# Gets all links in an html string that link to a page within the given domain
def get_links(html, base_url):
	links = set()
	s = BeautifulSoup(html, "html.parser")
	a = s.find_all('a')
	# for each 'a' element found
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

# Main runner function
def run():
	# get url
	base_url = "http://www.trincoll.edu/"
	depth_max = 4

	# initializes queue and set of emails and links
	q = Queue.Queue()
	all_links = set()
	all_emails = set()

	# start crawling from base_url
	q.put(base_url)
	all_links.add(base_url)

	# keeps track of depth of page-tree
	depth = 1;
	
	# while there are remaining pages to crawl
	while not q.empty():
		# get html string of current page
		url = q.get()
		print url
		html = get_file(url)
		
		# extract emails addresses
		emails = get_emails(html)

		# find href links
		links = get_links(html, base_url)

		# for each link found
		for link in links:
			# check if not already visited and if depth doesnt exceed max-depth
			if link not in all_links and depth < depth_max:
				# add to queue
				q.put(link)

		# update set
		all_emails.update(emails)
		all_links.update(links)

		# increment depth
		depth = depth + 1

	# output emails, if any
	for e in all_emails:
		print e

run()
	
	


