import requests
from bs4 import BeautifulSoup
from io import BytesIO
from PyPDF2 import PdfReader
import json

with open("keywords.json", "r") as f:
    keywords = json.load(f)

keywords = keywords['High_Priority']

main_url = "https://www.gov.pl/web/gif/wiadomosci"
root_url = 'https://www.gov.pl'
response = requests.get(main_url)

notifications = []

def get_all_notification_news_section():

    pattern_one = 'https://www.gov.pl/web/gif/wiadomosci?page='
    pattern_two = '&size=10'

    counter = 1
    response = requests.get(pattern_one + str(counter) + pattern_two)
    hrefs = []
    soup = BeautifulSoup(response.text, 'html.parser')

    while True:
        #art-prev art-prev--near-menu
        soup = BeautifulSoup(response.text, 'html.parser')
        if soup.find('input',  {'id': 'js-pagination-page'}).get('value') != str(counter):

            break
        page_content = response.text
        soup = BeautifulSoup(page_content, 'html.parser')
        article_section = soup.find_all("div", class_="art-prev art-prev--near-menu")
        soup = BeautifulSoup(str(article_section), 'html.parser')
        all_hrefs = soup.find_all('a')
        href = [a.get('href') for a in all_hrefs]
        full_href = [root_url + h for h in href]
        hrefs.extend(full_href)

        counter += 1

        response = requests.get(pattern_one + str(counter) + pattern_two)

    return hrefs

def get_text_from_url(hrefs):

    for href in hrefs:

        print(href)
        response_href = requests.get(href)
        soup = BeautifulSoup(response_href.text, 'html.parser')
        title = soup.find_all("main")
        #print(f'Title: {title}')
        soup_title = BeautifulSoup(str(title), 'html.parser')
        title = soup.find_all("h2")[0].get_text()
        if high_priority_or_low(title):
            priority = "high priority"
        else:
            priority = "low priority"
        try:
            data = soup_title.find("p", class_="event-date").get_text()
        except AttributeError:
            print("NoneType")

        print(f'Data: {data}')
        content = soup.find_all("div", class_="article-area main-container")
        soup = BeautifulSoup(str(content), 'html.parser')
        text = soup.find_all("p")[1]
        text= [t.get_text() for t in text]
        notifications.append({'title' : title, 'data' : data, 'author' : None, 'text' : text, 'priority' : priority, 'url' : href, 'pdf_url' : None})


def high_priority_or_low(title):

    title = title.lower()
    for keyword in keywords:
        if keyword in title :
            return True

    return False

news = get_all_notification_news_section()


print(notifications)