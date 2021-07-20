import requests
from bs4 import BeautifulSoup
from dataclasses import dataclass, field


@dataclass()
class Chapter:
    name: str
    link: str
    content: list = field(default_factory=list)


@dataclass()
class Book:
    title: str
    category: str
    description: str
    chapters: list = field(default_factory=list)


headers = {'user-agent': 'my-agent/1.0.1'}


def chapterTextExtractor(link: str):
    story = []
    l = requests.get(link, headers=headers)
    lSoup = BeautifulSoup(l.content, 'html.parser')

    for c1 in lSoup.find_all("pre"):
        for c2 in c1.find_all("p"):
            story.append(c2.getText())

    return story


def chaptersInfoExtractor(link: str):
    l = requests.get(link, headers=headers)
    lSoup = BeautifulSoup(l.content, 'html.parser')

    chapters = []

    for c1 in lSoup.find_all('a', href=True):
        for c2 in c1.find_all("div", {"class": "part-title"}):
            chapters.append(
                Chapter(
                    c2.getText().strip()
                    , c1['href'], chapterTextExtractor("https://www.wattpad.com" + c1['href'])))

    return chapters


def metadataBookExtractor(link: str):
    l = requests.get(link, headers=headers)
    lSoup = BeautifulSoup(l.content, 'html.parser')

    title = ""
    genre = ""
    description = ""

    for c1 in lSoup.find_all("div", {"class": "media-item story-info"}):
        # print(c1)
        title = c1.find("h3").getText()
        genre = c1.find("a").getText()
        description = c1.find("p", {"class": "item-description"}).getText()
    chpts = chaptersInfoExtractor(link)

    return Book(title, genre, description, chpts)
