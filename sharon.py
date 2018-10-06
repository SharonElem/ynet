import urllib
import urllib.request
import bs4
import codecs
import csv
import os
import matplotlib.pyplot as plt
import urllib.parse
from googlesearch import search

url = "https://www.ynet.co.il"
html = urllib.request.urlopen(url).read()
soup = bs4.BeautifulSoup(html, 'html.parser')

# Getting the data from "ynet"
for script in soup(["script", "style"]):
    script.extract()
text = soup.get_text()
lines = (line.strip() for line in text.splitlines())
chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
text = '\n'.join(chunk for chunk in chunks if chunk)
text = text.split('\n')
with codecs.open(os.path.join(os.getcwd(), 'ynet.csv'), 'w', encoding='UTF-16') as csv_file:
    writer = csv.writer(csv_file)
    for item in text:
        writer.writerow([item])


# Going through all articles and classifying by tags

i = 0
tags_counter={}
links = soup.find_all('a')
for l in links:
    link = links[i]
    i = i+1
    url = link.get("href")
    if url is not None:
        if url.find("article") != -1:
            if url.find("www") == -1:
                url = "https://www.ynet.co.il"+url
            if url.find("http") == -1:
                url="https"+url
            try:
                html = urllib.request.urlopen(url).read()
                soup = bs4.BeautifulSoup(html, 'html.parser')
                tags = soup.findAll('a')
                for tag in tags:
                    tag = tag.get('title')
                    if tag is None:
                        break
                    if tag in tags_counter:
                        tags_counter[tag] = tags_counter[tag]+1
                    else:
                        tags_counter[tag] = 1
            except IOError:
                # exception handling goes here if you want it
                pass

names = list(tags_counter.keys())
values = list(tags_counter.values())
i = 0
for name in names:
    names[i] = name[::-1]
    i = i+1
plt.figure(figsize=(25, 25))  # width:20, height:3
plt.bar(range(len(names)), values, align='edge', width=0.3, color='green')
plt.xticks(rotation=90)
plt.xticks(range(1, len(names)+1), names, size='small')
plt.title("How Articles Were Tagged Today?")

plt.savefig('How_Articles_Were_Tagged_Today.png')

# Going through all links that are not ynet and checking who is the owner

Owner_Of_Published_Website = {}
for l in links:
    url = l.get("href")
    if url is not None:
        if url.find("ynet") == -1 and url.find("http") != -1:
            splurl = url.split(".")
            Owner_Of_Published_Website[splurl[1]]=0
print(Owner_Of_Published_Website)
for web in list(Owner_Of_Published_Website.keys()):
    query = "בעלים" + web
    for j in search(query, tld="com", num=1, stop=1, pause=2):
       print(j)
# if ("pdf" not in j) and ("linkedin" not in j) and ("rol" not in j) and ("reverso" not in j):
       try:
            html = urllib.request.urlopen(j).read()
            soup = bs4.BeautifulSoup(html, 'html.parser')
            for script in soup(["script", "style"]):
                script.extract()
            text = soup.get_text()
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = '\n'.join(chunk for chunk in chunks if chunk)
            text = text.split('\n')
            Owner_Of_Published_Website[web]=text
       except IOError:
            # exception handling goes here if you want it
            pass

with codecs.open(os.path.join(os.getcwd(), 'Owner_Of_Published_Website.csv'), 'w', encoding='UTF-16') as csv_file:
    writer = csv.writer(csv_file)
    for key, value in Owner_Of_Published_Website.items():
        writer.writerow([key, value])

# print(Owner_Of_Published_Website)