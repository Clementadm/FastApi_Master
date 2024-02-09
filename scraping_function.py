from bs4 import BeautifulSoup
import requests

def scrap_url_user(url_input):
    page = requests.get(url_input)
    soup = BeautifulSoup(page.content, 'html.parser')
    print(soup.title)