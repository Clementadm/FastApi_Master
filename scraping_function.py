from bs4 import BeautifulSoup
import requests, re

# function that get the url input by the user and scrap the content of the page
def scrap_url_user(url_input):
    page = requests.get(url_input)

    # If the request succeed then we start to scrap
    if page.status_code == 200:
        soup = BeautifulSoup(page.content, 'html.parser')
        title_page = soup.title
        content = soup.get_text()
        # content = re.sub(r'\n{2,}', '\n', str(content))
        print(f'{content}')
    else :
        print("Error when scraping ", str(url_input), " check the scrap_url_user function")


    # pas prendre en compte les \n ? ==> perte de notion de titre, contenu, ... 