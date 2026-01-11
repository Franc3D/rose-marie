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

    content_table = extract_bdg(file_path)


def extract_bdg(file_path):
    reader = PdfReader(file_path)
    for page in reader.pages:
        print(page.extract_text())

def generate_order(content_table):
    pass

def generate_ISBN(content_table):
    pass

if __name__ == "__main__":
    read_bdg()