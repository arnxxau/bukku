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
    link: str
    chapters: list = field(default_factory=list)


headers = {'user-agent': 'my-agent/1.0.1'}
w = requests.get(
    "https://www.wattpad.com/1025739380-l%E1%B4%80-%CA%9C%C9%AA%E1%B4%8A%E1%B4%80-%CA%99%C9%AA%E1%B4%8F%CA%9F%E1%B4%8F%C9%A2%C3%AD%E1%B4%84%E1%B4%80-%E1%B4%85%E1%B4%87-r%E1%B4%87%C9%A2%C9%AA%C9%B4%E1%B4%80%CA%9F%E1%B4%85-h%E1%B4%80%CA%80%C9%A2%CA%80%E1%B4%87%E1%B4%87%E1%B4%A0%E1%B4%87s-capitulo",
    headers=headers)

soup = BeautifulSoup(w.content, 'html.parser')

li = "https://www.wattpad.com/196238516-mi-jefe-capitulo-1-el-primer-vistazo"

hi = soup.find_all("pre")


mydivs = soup.find_all('a', href=True)


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
                    , c1['href'], chapterTextExtractor("https://www.wattpad.com"+c1['href'])))

    return chapters


def metadataBookExtractor(link: str):
    l = requests.get(link, headers=headers)
    lSoup = BeautifulSoup(l.content, 'html.parser')

    title = ""
    type = ""
    description = ""

    for c1 in lSoup.find_all("div", {"class": "media-item story-info"}):
        # print(c1)
        title = c1.find("h3").getText()
        type = c1.find("a").getText()
        description = c1.find("p", {"class": "item-description"}).getText()
    chpts = chaptersInfoExtractor(link)

    return Book(title, type, description, chpts)

f = open("text.txt", "a")

m = metadataBookExtractor(li)

print(m.chapters[3])

f.write(f"{m.title} \n")
for chapter in m.chapters:
    f.write(f"{chapter.name} \n")
    for line in chapter.content:
        f.write(f"{str(line)} \n")



