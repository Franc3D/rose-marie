#import urllib
import requests
from bs4 import BeautifulSoup

def main():
    
    #FETCH THE PAGE
    url = "https://www.leslibraires.ca/livres/petit-pas-9782925416760" #Test URL
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers)
    html = response.text

    #PARSE THE HTML
    soup = BeautifulSoup(html, "html.parser")

    items = soup.find_all("div", class_="product__description") 
    print(len(items))

    for item in items:
        title = item.find("div", class_="d-inline text-normalizer").get_text(strip=True)
        print("*")
        print(title)

    #Figure out how to open a webpage through a .py file 
    #The program type is called a web scraper
    #The Beautiful soup library is especially well suited for this task 


if __name__ == "__main__":
    main()