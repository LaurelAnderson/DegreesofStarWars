#Program by Laurel Anderson
import requests
import re 
from bs4 import BeautifulSoup
from collections import deque


#returns a random page that you can get the url out of. 
def get_random_page(): 
	r = requests.get('https://en.wikipedia.org/wiki/Special:Random')
	return r

#looks through the links and returns only valid ones. 
def filter_links(href):
	if href:
		if re.compile('^/wiki/').search(href):
			if not re.compile('/\w+:').search(href):
				if not re.compile("#").search(href):
					return True
	return False


def search(vertex):
		
	start = vertex.url

	queue = deque([start])
	level = {start:0}
	parent = {start:None}
	
	#start BFS	
	while queue:
		
		#get url from queue.
		v = queue.popleft()
		#get contents of popped url
		w = requests.get(v)
		#send page content through BeautifulSoup
		page = BeautifulSoup(w.text, 'html.parser')
		body = page.find(id="bodyContent")
		
		#Get all the connecting vertices
		for link in body.find_all('a', href=filter_links):
			url = 'https://en.wikipedia.org' + link.get('href')
			title = link.string
			#Check to see if vertex needs to be put in the queue
			if url not in level and level[v] < 5:
				queue.append(url)
				level[url]=level[v]+1
				parent[url]=v
		
				#Check every url to see if it is the one we want
				if url == star_wars:
					return parent

	#return if you cannot find star wars in less then 6 jumps
	return parent

#Start of the program
star_wars = 'https://en.wikipedia.org/wiki/Star_Wars'
start = get_random_page()

#Send the start vertex to the BFS method 
outcome = search(start)

if star_wars in outcome:
	
	#create a list of the reverse url path
	path = [star_wars]

	i = outcome[star_wars]
	while True:
		path.append(i)
		i = outcome[i]
		if i == None:
			break

#Get the list in the right direction
path.reverse()

#get and print the titles of each of the webpages. 
for i in path:

	page = requests.get(i)
	soup = BeautifulSoup(page.text, 'html.parser')
	title = soup.find('title')
	print(title.string + ': ' + i)
	
	

	

