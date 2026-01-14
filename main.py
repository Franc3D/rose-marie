import cegep
import bdg
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
    
    else:
        input("Cette option n'est pas valide, appuyez sur une touche pour quitter...")
        
    
    

if __name__ == "__main__":
    main()