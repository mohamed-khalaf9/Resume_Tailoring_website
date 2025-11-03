from bs4 import BeautifulSoup




def clean_text(text):
    soup = BeautifulSoup(text, 'html.parser')
    text = soup.get_text()

    text = ' '.join(text.split())

    return text


