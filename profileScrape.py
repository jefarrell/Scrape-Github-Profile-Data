# John Farrell 2015
# Scrape Github profile data
### Creates CSV file with commit data from profile data visualization
### Creates JSON file with basic profile information and highlights
### Downloads avatar photo

import urllib
from bs4 import BeautifulSoup
import sys
import csv
import json
import os
import shutil

output = []
gitUser = sys.argv[1]
url = 'http://github.com/' + gitUser
data = urllib.urlopen(url).read()
soup = BeautifulSoup(data)

### make a new folder for each user
# os.getcwd()
# os.mkdir(gitUser)
# os.chdir(gitUser)



### get commit history data, write to CSV
f = open(gitUser + '.csv', 'wt')

days = soup.findAll('rect', {'class' : 'day'})
writer = csv.writer(f)
writer.writerow(('Commit Count', 'Date'))


for day in days:
	count = day['data-count']
	date = day['data-date']
	writer.writerow((count,date))


f.close()




### get avatar
def download_image(imageurl):
	print 'downloading ', imageurl
	#formatting the url to get full-sized images
	DLurl = imageurl.replace("?v=3&s=460", "")
	filename = gitUser + ".jpeg"
	urllib.urlretrieve(DLurl,filename)


### get profile info
fullname = soup.find('span', {'class' : 'vcard-fullname'}).string
username = soup.find('span', {'class' : 'vcard-username'}).string
location = soup.find('li', {'class' : 'vcard-detail'})['title']
joined = soup.find('time', {'class' : 'join-date'}).string
followers = soup.find('strong', {'class' : 'vcard-stat-count'}).string
streak = soup.findAll('span', {'class' : 'contrib-number'})[1].text


### get repo info
repos = soup.findAll('div', {'class' : 'columns popular-repos'})
for reps in repos:
	popular = reps.findAll('div', {'class' : 'column one-half'})[0]
	contributed = reps.findAll('div', {'class' : 'column one-half'})[1]
	
	pops = popular.find('a', {'class' : 'mini-repo-list-item css-truncate'})['href']
	popstars = popular.find('span', {'class' : 'stars'}).text.strip()

	cons = contributed.find('a', {'class' : 'mini-repo-list-item css-truncate'})['href']
	constars = contributed.find('span', {'class' : 'stars'}).text.strip()


### write profile info to JSON
output.append({'full name': fullname, 'user name': username, 'location': location, 'joined': joined, 'followers': followers, 'popular repo': pops, 'popular stars': popstars, 'contributed to': cons, 'contributed stars': constars, 'longest streak': streak})

with open(gitUser + ".json", "w") as outputfile:
	json.dump(output, outputfile, indent=2)
	print 'dumping ', outputfile

### 
imgLoc = soup.find("img")['src']
download_image(imgLoc)

