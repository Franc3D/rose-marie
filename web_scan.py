#import urllib
import requests
from bs4 import BeautifulSoup
import json
import re

def scan_memento():

    session = requests.Session()

    header = {
        "user-Agent": "Mozilla/5.0",
        "Referer": "https://www.mementolivres.com/"
    }

    #Warm-up request
    session.get("https://www.mementolivres.com/", headers=header)

    #login to Memento (it uses ASP.NET WebForms)
    login_url = "https://www.mementolivres.com/Login.aspx"

    r = session.get(login_url, headers=header)
    soup = BeautifulSoup(r.text, "html.parser")

    print(r.text)

    print("***")
    print("form" in r.text.lower())
    print("input" in r.text.lower())
    for keyword in ["txtEmail", "txtPassword", "Email", "Password", "__VIEWSTATE"]:
        print(keyword, keyword.lower() in r.text.lower())
    for tag in soup.find_all("input"):
        print(tag.get("id"), tag.get("name"))

    print("***")
    for tag in soup.find_all("input"):
        print(tag)


    payload = {
        "__VIEWSTATE": soup.find("input", {"id": "__VIEWSTATE"})["value"],
        "__VIEWSTATEGENERATOR": soup.find("input", {"id": "__VIEWSTATEGENERATOR"})["value"],
        "__EVENTVALIDATION": soup.find("input", {"id": "__EVENTVALIDATION"})["value"],

        "txtEmailAddress": "info@librairierosemarie.com",
        "pasPassword": "liroma1",
        "btnLogin": "Connexion"
    }

    #Actually logging in
    session.post(login_url, data=payload)
    
    #FETCH THE PAGE
    #url = "https://www.leslibraires.ca/livres/petit-pas-9782925416760" #Test URL
    url = input("SVP entrez l'adresse web à analyser : ")
    #headers = {"User-Agent": "Mozilla/5.0"}

    response = session.get(url)#, headers=headers)
    html = response.text

    print(html)

    #PARSE THE HTML
    soup = BeautifulSoup(html, "html.parser")

    items = soup.find_all("div", class_="product__description") 
    print("there is", len(items), "in the items variable")

    for item in items:
        title = item.find("div", class_="d-inline text-normalizer").get_text(strip=True)
        print("*")
        print(title)

    #Figure out how to open a webpage through a .py file 
    #The program type is called a web scraper
    #The Beautiful soup library is especially well suited for this task 


#liste de problèmes à régler :
# - utiliser l'outil de recherche du sute web désiré
# - Se connecter à memento

#Utiliser l'outil de recherche pour trouver un livre sur LesLibraires.ca
def find_url_old(): #On LesLibraires.ca

    isbn = input("What is the ISBN you want to find in LesLibraires.ca : ")

    search_url = f"https://www.leslibraires.ca/recherche/?isbn={isbn}"

    session = requests.Session()
    response = session.get(search_url, allow_redirects=True)

    final_url = response.url
    print(final_url)
    input("Appuyez sur ENTER pour continuer...")
    #Trouver pourquoi il redirige vers catalogue/?isbn=...
    #Un script javascript peut être ?

import requests

def find_url():
    isbn = input("ISBN: ")

    url = f"https://www.booksellers.ca/api/search/products?keywords={isbn}&page=1"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    r = requests.get(url, headers=headers)
    data = r.json()

    if "products" in data and data["products"]:
        product = data["products"][0]
        real_url = "https://www.leslibraires.ca" + product["url"]
        print(real_url)
    else:
        print("No result found.")


def debug_html(isbn):
    url = f"https://www.leslibraires.ca/catalogue?isbn={isbn}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    r = requests.get(url, headers=headers)
    print(r.text[:2000])  # print first 2000 chars


if __name__ == "__main__":
    find_url()