# CheveretoDownloader
# v0.2
# FeelsGeniusMan
import requests, sys, os, re
from bs4 import BeautifulSoup

# define some values for later
i = 1
pages = []
urls = []
correctedlinks = []

# Tool intro and ask user for an album URL
print('CheveretoDownloader')
inp = input('[x] Enter the Album (Page) URL and press enter: ').strip()

# find the Album name from the meta tag og:title
Albuminp = requests.get(inp)
searched = BeautifulSoup(Albuminp.text, 'html.parser')
dir = searched.find("meta", {"property": "og:title"}).attrs['content']

# create a directory with the album name (dir) if no directory exists
try:
    os.mkdir(dir)
    print(f'[~] Directory', dir, 'created.')
except OSError as error:
    print(f'[~] Directory', dir, 'already exists')

# change to the new directory so that files are saved in it
os.chdir(dir)


print(f'[~] Scraping pages of {dir}:')
pages.append(inp)
print(inp)
while i < 2:
    # searches for links within the page
    reqs = requests.get(inp)
    soup = BeautifulSoup(reqs.text, 'html.parser')
    # searches for next page link
    li = soup.find("li", {'class': 'pagination-next'})
    if li == None:
        i=2
    else:
        for child in li.children:
            nextURL = child.get("href")
            print(nextURL)
            pages.append(nextURL)
        if not nextURL:
            i=2
        else:
            inp = nextURL


print('[~] Page links scraped')

# creates a session of the html request module so that multiple downloads run quickly
s = requests.Session()
print ('[~] Scraping image links')

# Removes blank links
for val in pages:
    if val != None :
        correctedlinks.append(val)

# Searches through links for image urls
for link in correctedlinks:
    with s.get(link) as r:
        # parses the html
        # searches for all image links in the html
        bs = BeautifulSoup(r.text, 'html.parser')
        new = bs.find('div', {'class': 'pad-content-listing'})
        es = [image["src"] for image in new.findAll("img")]
        for e in es:
            u = e.replace('.md.', '.').replace('.th.', '.')
            # caches the image urls in a list
            urls.append(u)
print(f'[~] Downloading {len(urls)} images')

excpts = 0
for u in urls:
    # gets the filename from the image url
    fn = u.split('/', 3)[3]
    print(f'[~] Saving - {fn}')
    try:
        with s.get(u) as r:
            with open(fn, 'wb') as o:
                # downloads in chunks to save memory
                for c in r.iter_content(chunk_size=8192):
                    o.write(c)
    except:
        print(f'[!] Error - {u}')
        # counts errors
        excpts += 1
        continue

print(f'[+] Album downloaded, {excpts} failed download(s)')
exitText = input("\nFinished. Press enter to quit.")
