import cegep
import bdg
import os
from PyPDF2 import PdfReader
#from cegep import read_cegep

def main():
    print("***Programme de listage de commande***")
    print("--------------------------------------")
    print("VEUILLEZ DÉPOSER LE DOCUMENT À TRAITER DANS LA FENÊTRE OU SÉLECTIONER L'UNE DES OPTIONS SUIVANTES...")
    print("--------------------------------------")
    print("Choisissez une option ci bas")
    print("1 -Cégep de l'Outaouais")
    print("2 -Bibliothèque de Gatineau (BdG)")
    print("3 -Futur projet")
    
    response = input("Entrez le chiffre de l'option désiré :")

    if response == "1":
        cegep.read_cegep()

    elif response == "2":
        bdg.read_bdg()

    elif response == "3":
        pass
    
    elif len(response) > 7:
        #Cleanup the path if in powershell
        response = normalize_path(response)
        #verify if the response is a valid path
        if os.path.exists(response):
            
            auto_manage_doc(response)
            
        else:
            print("Ce dossier est invalide.")
            input("Appuie sur ENTER pour continuer...")
        

    
    else:
        input("Cette option n'est pas valide, appuyez sur une touche pour quitter...")
        

def auto_manage_doc(filepath):
    #This will automatically read the doc in the path and activate the proper .py function to treat it
    #detect extention 
    extension = filepath[filepath.rfind("."):]

    if extension == ".txt": #has to be Cegep
        with open(filepath, "r", encoding="cp1252") as file:
            lines = file.readlines()
            if "-- BON DE COMMANDE #" in lines[3]:
                cegep.read_cegep(filepath)
            else:
                print("Ce fichier ne correspond pas à aucun format valide")
                input("Appuyez sur ENTER pour quitter...")

    elif extension == ".pdf": #Has to be BdG
        file = PdfReader(filepath)

        first_page = file.pages[0].extract_text()
        lines = first_page.splitlines()

        identifier = "(Merci d'indiquer le numéro du BC dans toute correspondance)"
        if lines[1] == identifier:
            bdg.read_bdg(filepath)
        
    #open and read the file
    #Identify what document it is
    #Call the proper .read_... function add the filepath to not have to redrop it in an input


def normalize_path(p):
    p = p.strip()
    if p.startswith("& '") and p.endswith("'"):
        return p[3:-1]
    elif p.startswith("\"") and p.endswith("\""):
        return p[1:-1]
    return p

if __name__ == "__main__":
    main()