# Mando's Chevereto Downloader Taking Elements from the Cyberdrop Gallery Downloader by Jules--Winnfield

import requests
import os
import re
from colorama import Fore, Style
from multiprocessing import Pool
from bs4 import BeautifulSoup, SoupStrainer
import multiprocessing
import settings


class Error(Exception):
    """Base class for exceptions in this module."""
    pass


class SizeError(Error):
    """Exception raised for errors in the input.
    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """

    def __init__(self, expression, message):
        self.expression = expression
        self.message = message


def log(text, style):
    # Log function for printing to command line
    print(style + str(text) + Style.RESET_ALL)


def clear():
    # Clears command window
    os.system('cls' if os.name == 'nt' else 'clear')


def download(passed_from_main):
    _path = passed_from_main[0]
    _item = passed_from_main[1]
    attempts = 1
    attemptsToTry = (settings.file_attempts + 1) if settings.file_attempts != 0 else 0
    try:
        while True:
            filename = _item[_item.rfind("/") + 1:]
            _url = _item

            if attemptsToTry != 0 and attempts >= attemptsToTry:
                log("        Hit user specified attempt limit" + " for " + filename + " skipping file", Fore.RED)
                break
            else:
                if attempts != 1:
                    log("        Retrying " + filename + "...", Fore.YELLOW)
                try:

                    response = requests.get(_url, stream=True)
                    incomingFileSize = int(response.headers['Content-length'])

                    if os.path.isfile(_path + str(filename)):
                        storedFileSize = os.path.getsize(_path + str(filename))
                        if incomingFileSize == storedFileSize:
                            log("           " + filename + " already exists.", Fore.LIGHTBLACK_EX)
                            break
                        else:
                            log("           " + filename + " already exists, but is corrupt", Fore.LIGHTBLACK_EX)
                            os.remove(_path + str(filename))

                    log("        Downloading " + filename + "...", Fore.LIGHTBLACK_EX)

                    with open(_path + str(filename), "wb") as out_file:
                        for chunk in response.iter_content(chunk_size=50000):
                            if chunk:
                                out_file.write(chunk)
                    del response
                    if os.path.isfile(_path + str(filename)):
                        storedFileSize = os.path.getsize(_path + str(filename))
                        if incomingFileSize == storedFileSize:
                            log("        Finished " + filename, Fore.GREEN)
                            break
                        else:
                            raise SizeError("File Size Specified: {} bytes, File Size Obtained: {} bytes".format(
                                incomingFileSize, storedFileSize), "These file sizes don't match")
                    else:
                        log("        Something went wrong" + " for " + filename, Fore.RED)
                        attempts += 1
                except Exception as e:
                    # log(e, Fore.RED)
                    os.remove(_path + str(filename))
                    log("        Failed attempt " + str(attempts) + " for " + filename, Fore.RED)
                    attempts += 1

    except Exception as e:
        print(e)
        print("Failed to Download")


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


if __name__ == '__main__':
    log("", Fore.RESET)

    response = requests.get("https://api.github.com/repos/MandoCoding/CheveretoDownloader/releases/latest")
    latestVersion = response.json()["tag_name"]
    currentVersion = "0.4"
    clear()
    if latestVersion != currentVersion:
        print("A new version of CheveretoDownloader is available\n"
              "Download it here: https://github.com/MandoCoding/CheveretoDownloader/releases/latest\n")

    headers = {'headers': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:51.0) Gecko/20100101 Firefox/51.0'}

    cpu_count = settings.threads if settings.threads != 0 else multiprocessing.cpu_count()
    downloadFolder = settings.download_folder

    if downloadFolder == "./Downloads/":
        if not os.path.exists(downloadFolder):
            os.makedirs(downloadFolder)
    else:
        if not os.path.exists(downloadFolder):
            log("The download folder specified (" + downloadFolder + ") does not exist ", Fore.RED)

    totalFiles = 0

    if os.path.isfile("URLs.txt"):
        print("URLs.txt exists")
    else:
        f = open("URLs.txt", "w+")
        print("URLs.txt created")

    if os.stat("URLs.txt").st_size == 0:
        print("Please put URLs in URLs.txt")

    file_object = open("URLs.txt", "r")
    for line in file_object:
        url = line.rstrip()

        Albuminp = requests.get(url)
        searched = BeautifulSoup(Albuminp.text, 'html.parser')
        AlbumName = searched.find(attrs={"data-text": "album-name"})
        url = AlbumName.get('href')

        html = requests.get(url, headers=headers)
        htmlAsText = html.text
        dirName = htmlAsText[htmlAsText.find("<title>") + 7:htmlAsText.find("</title>")]
        rstr = r"[\/\\\:\*\?\"\<\>\|\.]"  # '/ \ : * ? " < > | .'
        dirName = re.sub(rstr, "_", dirName)
        dirName += "/"

        dirRemove = searched.find("meta", {"property": "og:site_name"}).attrs['content']
        dirRemove = " - " + dirRemove
        dirName = dirName.replace(dirRemove, '')

        path = downloadFolder+dirName

        print("\n======================================================\n")

        print("\nCollecting file links from " + url + "...")
        links = Extrair_Links(url)

        if links is None:
            print()
            input(url + " Couldn't find pictures.")
            exit()

        print()
        print("       URL       " + url)
        print("       DIR       " + path)
        print()
        if not (os.path.isdir(path)):
            try:
                os.mkdir(path)
                print()
                log("Created directory {dir}".format(dir=path), Fore.GREEN)
            except OSError as e:
                log("Creation of directory {dir} failed: {err}".format(dir=path, err=e), Fore.RED)
        print()

        pass_to_func = []
        for link in links:
            pass_to_func.append([path, link])

        print("Downloading " + str(len(pass_to_func)) + " files...")
        pool = Pool(processes=cpu_count)
        proc = pool.map_async(download, pass_to_func)
        proc.wait()
        pool.close()

    exitText = input("\nFinished. Press enter to quit.")
