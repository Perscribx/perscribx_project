from types import NoneType

import requests
from bs4 import BeautifulSoup
from io import BytesIO
from PyPDF2 import PdfReader

from machine_learning.scraping_news_section import notifications

main_url = "https://www.gov.pl/web/gif/komunikaty"
root_url = 'https://www.gov.pl'
response = requests.get(main_url)

notifications = []

def all_notifications_urls():
    pattern_one = 'https://www.gov.pl/web/gif/komunikaty?page='
    pattern_two = '&size=10'
    counter = 1
    response = requests.get(pattern_one + str(counter) + pattern_two)
    hrefs = []
    soup = BeautifulSoup(response.text, 'html.parser')
    while True:
        soup = BeautifulSoup(response.text, 'html.parser')
        if soup.find_all('input',  {'id': 'js-pagination-page'})[0].get('value') != str(counter):
            break
        page_content = response.text
        soup = BeautifulSoup(page_content, 'html.parser')
        all_hrefs = soup.find_all('a')

        href = [a.get('href') for a in all_hrefs]
        href = [hrefs.append(a) for a in href if '/web/gif/komunikat-glownego-inspektora-farmaceutycznego-z-dnia-' in a]

        counter += 1

        response = requests.get(pattern_one + str(counter) + pattern_two)

    return hrefs

def get_text_from_pdf_from_url(url):

    response_pdf = requests.get(url)
    if response_pdf.status_code == 200:

        read_pdf = BytesIO(response_pdf.content)
        pdf_reader = PdfReader(read_pdf)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"

    return text

#PDF URL
def get_pdf_url(site_url):

    full_path = root_url + site_url
    response_pdf_site = requests.get(full_path)
    soup_pdf = BeautifulSoup(response_pdf_site.content, 'html.parser')
    a_list = soup_pdf.find_all('a', class_='file-download')
    href = [a.get('href') for a in a_list][0]
    return root_url + href

def get_notification_meta_data(site_url):
    full_path = root_url + site_url
    response_data = requests.get(full_path)
    soup_data = BeautifulSoup(response_data.text, 'html.parser')

    metadata =  [x.get_text() for x in soup_data.find_all('dd')]

    if metadata :
        metadata = metadata[0].split()
        return metadata[0], metadata[1], metadata[2] + " " + metadata[3]

    return None
def get_title(site_url):

    full_path = root_url + site_url
    response_data = requests.get(full_path)
    soup_data = BeautifulSoup(response_data.text, 'html.parser')
    intro = [x.get_text() for x in soup_data.find_all('p', class_='intro')]
    if intro:
        return intro[0]
    return None

def all_notifications():
    urls = all_notifications_urls()
    for url in urls:
        pdf_url = get_pdf_url(url)
        try:
            data, time, author = get_notification_meta_data(url)
        except Exception:
            data = None
            time = None
            author = None
        title = get_title(url)
        pdf_text = get_text_from_pdf_from_url(pdf_url)
        notifications.append({'title' : title, 'data' : data, 'author' : author, 'text' : pdf_text, 'priority' : "high priority", 'url' : root_url +  url, 'pdf_url' : pdf_url})



all_notifications()
print(notifications)