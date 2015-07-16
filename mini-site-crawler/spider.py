import sys
import httplib2
from bs4 import BeautifulSoup, SoupStrainer
import datetime

def log_std(msg):
	now = datetime.datetime.now()
	std_time = now.isoformat()
	print(std_time,' ',msg)
	
def get_response(url,log):
	try:
		http = httplib2.Http()
		status, response = http.request("http://www.google.com")
		return response
	except httplib2.ServerNotFoundError:
		log("Error retrieving "+url)

def find_links(response):
	list = []
	for link in BeautifulSoup(response, "html.parser", parse_only=SoupStrainer('a')):
		if link.has_attr('href'):
			list.append(link['href'])
	return list

class Spider:
	def __init__(self, startURL, log=None):
		self.URLs = set()
		self.URLs.add(startURL)
		self.include = startURL
		self._links_to_process = [startURL]
		if log is None:
			self.log = log_std
		else:
			self.log = log	

	def run(self):
		while self._links_to_process:
			url = self._links_to_process.pop()
			self.log("Retrieving:"+url)
			self.process_page(url)
	
	def is_url_in_site(self,link):
		#print(link + "-" + self.include + "-" + str(link.startswith(self.include)))
		return link.startswith(self.include)
		
	def process_page(self,URL):
		response = get_response(URL,self.log)
		for link in find_links(response):
			self.log("Checking: "+link)
			if link not in self.URLs and not self.is_url_in_site(link):
				self.URLs.add(link)
				self._links_to_process.append(link)
	
if __name__ == '__main__':
	startURL = sys.argv[1]
	spider = Spider(startURL)
	spider.run()
	for URL in sorted(spider.URLs):
		print(URL)