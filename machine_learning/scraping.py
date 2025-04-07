import requests
from bs4 import BeautifulSoup
from io import BytesIO
from PyPDF2 import PdfReader


main_url = "https://www.gov.pl/web/gif/komunikaty"
root_url = 'https://www.gov.pl'
response = requests.get(main_url)

def all_notifications_urls():
    if response.status_code == 200:
        page_content = response.text
        soup = BeautifulSoup(page_content, 'html.parser')
        all_hrefs = soup.find_all('a')

        hrefs = [a.get('href') for a in all_hrefs]
        href_notifications = [x for x in hrefs if '/web/gif/komunikat-glownego-inspektora-farmaceutycznego-z-dnia-' in x]

        print(href_notifications)

def get_text_from_pdf_from_url(url):

    response_pdf = requests.get(url)
    if response_pdf.status_code == 200:

        read_pdf = BytesIO(response_pdf.content)
        pdf_reader = PdfReader(read_pdf)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"

    return text

def get_pdf_url(site_url):

    full_path = root_url + site_url
    response_pdf_site = requests.get(full_path)
    soup_pdf = BeautifulSoup(response_pdf_site.content, 'html.parser')
    a_list = soup_pdf.find_all('a', class_='file-download')
    href = [a.get('href') for a in a_list][0]
    return root_url + href

def get_publication_date(site_url):

    full_path = root_url + site_url
    response_data = requests.get(full_path)
    soup_data = BeautifulSoup(response_data.text, 'html.parser')
    data = [x.get_text() for x in soup_data.find_all('p', class_='event-date')]

    return data[0]


all_notifications_urls()
url_pdf = get_pdf_url('/web/gif/komunikat-glownego-inspektora-farmaceutycznego-z-dnia-20-marca-2025-r')
text_from_pdf = get_text_from_pdf_from_url(url_pdf)

#get_text_from_pdf_from_url('/attachment/070a2fc5-7cb5-468e-8d6b-d73b4e3db12f')


print(get_publication_date('/web/gif/komunikat-glownego-inspektora-farmaceutycznego-z-dnia-20-marca-2025-r'))