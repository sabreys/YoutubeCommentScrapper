# -*- coding: utf-8 -*-
"""get_comments.py
this program  gets youtube live stream comments and write to file.
usage:
python get_comments.py "https://www.youtube.com/live_chat?is_popout=1&v=QR35MUnRUuE" "filename" 1

notice: link must be a chat link. not a video link.  "1" is the time that how many minutes you want to record.
@author sabreys
"""

from selenium import webdriver
import time
import sys
from bs4 import BeautifulSoup
from ordered_set import OrderedSet


class Comment:
    def __init__(self, name, text):
        self.name = name
        self.text = text

    def __str__(self):
        return self.name + ":" + self.text

    def __hash__(self):
        return hash(self.name + self.text)

    def __eq__(self, other):
        return self.name == other.name and self.text == other.text


def createHeadlessFirefoxBrowser():
    print("Initializing browser...")
    options = webdriver.FirefoxOptions()
    options.add_argument('--headless')
    return webdriver.Firefox(options=options, executable_path="C:/adb/geckodriver.exe")


def getSourcetWithBrowser(ytlink):
    browser.get(ytlink)
    source = browser.page_source
    return source


def getcomments(source):
    soup = BeautifulSoup(source, 'html.parser')
    comments = soup.find_all("yt-live-chat-text-message-renderer")

    for comment in comments:
        packet = comment.find("div", {"id": "content"})
        name = packet.find("span", {"id": "author-name"}).text
        text = packet.find("span", {"id": "message"}).text
        commentSet.add(Comment(name, text))


def writeCommentsToFile(filename):
    f = open(filename + ".txt", "a", encoding='utf-8')
    print("writing...")
    for x in commentSet:
        f.write(str(x) + "\n")
    f.close()


def startSession(ytlink, filename, duraction):
    print("it will take " + duraction + " minute")

    for i in duraction * 6:
        source = getSourcetWithBrowser(ytlink)
        getcomments(source)
        time.sleep(10)


browser = createHeadlessFirefoxBrowser()
commentSet = OrderedSet()


def main(ytlink, filename, duractiom):
    print("please wait...")
    startSession(ytlink, filename, duractiom)
    writeCommentsToFile(filename)
    browser.close()
    print("Mission Completed.")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])
