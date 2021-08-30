import requests
import os
from bs4 import BeautifulSoup, SoupStrainer

def Extrair_Links(u):
    # Extract links from gallery
    try:
        # create request, and soup
        url = u
        page = requests.get(url)
        data = page.text
        soup = BeautifulSoup(data, features="html5lib")
        links = []
        pages = []
        correctedlinks = []
        i = 1
        inp = u
        pages.append(inp)
        print(inp)
        while i < 2:
            # searches for links within the page
            reqs = requests.get(inp)
            soup = BeautifulSoup(reqs.text, 'html.parser')
            # searches for next page link
            li = soup.find("li", {'class': 'pagination-next'})
            if li == None:
                i = 2
            else:
                for child in li.children:
                    nextURL = child.get("href")
                    print(nextURL)
                    pages.append(nextURL)
                if not nextURL:
                    i = 2
                else:
                    inp = nextURL

        # Removes blank links
        for val in pages:
            if val != None:
                correctedlinks.append(val)

        # Searches through links for image urls
        s = requests.Session()
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
                    links.append(u)
        linksP = list(dict.fromkeys(links))

    except Exception as e:
        print(e)
        return None
    else:
        return linksP