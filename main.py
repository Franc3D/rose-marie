import cegep
import bdg
import os
#from cegep import read_cegep

def main():
    print("***Programme de listage de commande***")
    print("--------------------------------------")
    print("Choisissez une option ci bas")
    print("1 -Cégep de l'Outaouais")
    print("2 -Bibliothèque de Gatineau (BdG)")
    
    response = input("Entrez le chiffre de l'option désiré :")

    if response == "1":
        cegep.read_cegep()

    elif response == "2":
        bdg.read_bdg()
    
    elif len(response) > 7:
        #Cleanup the path if in powershell
        response = normalize_path(response)
        #verify if the response is a valid path
        if os.path.exists(response):
            auto_manage_doc(response)
            
        else:
            print("This path is invalid")
            input("Press any key to exit...")
        

    
    else:
        input("Cette option n'est pas valide, appuyez sur une touche pour quitter...")
        

def auto_manage_doc(filepath):
    #This will automatically read the doc in the path and activate the proper .py function to treat it
    print("auto manage doc")
     #todo
    #detect extention 
    extension = filepath[filepath.rfind("."):]

    if extension == ".txt":
        pass
    elif extension == ".pdf":
        pass
        
    #open and read the file
    #Identify what document it is
    #Call the proper .read_... function add the filepath to not have to redrop it in an input


def normalize_path(p):
    p = p.strip()
    if p.startswith("& '") and p.endswith("'"):
        return p[3:-1]
    return p

if __name__ == "__main__":
    main()