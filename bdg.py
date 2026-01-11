from PyPDF2 import PdfReader
import config

def read_bdg():
    print()
    print("PROGRAMME D'EXTRACTION DU BON DE COMMANDE DE LA BIBLIO DE GATINEAU")
    print("===============================================")
    print("VEUILLEZ DÉPOSER UN FICHIER À EXTRAIRE")
    print("===============================================")
    print()

    
    file_path = input("Déposez le fichier dans le fenêtre ou inscrivez le chemin du fichier à traiter : ")
    file_path = normalize_path(file_path) #Fixes the filepath if used in PowerShell

    content_table = extract_bdg(file_path)

def normalize_path(p):
    p = p.strip()
    if p.startswith("& '") and p.endswith("'"):
        return p[3:-1]
    return p

def extract_bdg(file_path):
    reader = PdfReader(file_path) #Need to figure out PdfReader

    no_bon_commande = ""
    order_table = []

    for page in reader.pages:
        #Skip the intro segment (grab the no_bon_commande once at least)

        #Every product uses 3 lines 
        #Divide every line 1 by spaces and look for 13 numbers, next index is QTY and then price
        #line 2 is the full title + " /"
        #line 3 got the total price at the end moderately useful (could always just qty + price)

def generate_order(content_table):
    pass

def generate_ISBN(content_table):
    pass

if __name__ == "__main__":
    read_bdg()