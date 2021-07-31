# CheveretoDownloader
# v0.1
# FeelsGeniusMan
import requests, sys, os, re
from bs4 import BeautifulSoup

i = 1

pages = []
print('CheveretoDownloader v0.1')
inp = input('[x] Enter the Album (Page) URL and press enter: ').strip()
test = inp
# regex, searches for the name in the album URL and prints it in the following line
id = re.search('(?<=album\/)(.*?)(?=\.)', inp)[0]
dir = id.replace("-", " ").title()
try:
    os.mkdir(dir)
    print(f'[~] Directory', dir, 'created.')
except OSError as error:
    print(f'[~] Directory', dir, 'already exists')
# creates a directory with the album name (id) in title case
os.chdir(dir)
# changes to the new directory so that files are saved in it

print(f'[~] Scraping pages of {id}:')
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


urls = []
# creates a session of the html request module so that multiple downloads run quickly
s = requests.Session()
print ('[~] Scraping image links')

correctedlinks = []
for val in pages:
    if val != None :
        correctedlinks.append(val)

for link in correctedlinks:
    with s.get(link) as r:
        # parses the html
        bs = BeautifulSoup(r.text, 'html.parser')
        # searches for all image links in the html
        es = bs.find_all('img')
        for e in es:
            # if the image link is not the logo, it looks for the "src" child of the img element
            if e['alt'] != 'PutMega':
                # replaces the url extension of "src" as the preview thumbnails have a different one
                u = e['src'].replace('.md.', '.').replace('.th.', '.')
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
