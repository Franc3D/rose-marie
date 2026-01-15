#This is the project for Rose-Marie
#Starting with the cegep .txt files
import config

#OUTPUT_ORDER=r"C:\Users\User\Documents\cegep_vente.txt"
#OUTPUT_LIST=r"C:\Users\User\Documents\cegep_liste_ISBN.txt"
#Need to make the output work in windows

alert = False


def read_cegep(filepath=""):
    print()
    print("PROGRAMME D'EXTRACTION DU BON DE COMMANDE DU CÉGEP")
    print("===============================================")
    print("VEUILLEZ DÉPOSER UN FICHIER À EXTRAIRE")
    print("===============================================")
    print()

    if filepath != "":
        file_path = filepath
    else:
        file_path = input("Déposez le fichier dans le fenêtre ou inscrivez le chemin du fichier à traiter : ")
        file_path = normalize_path(file_path) #Fixes the filepath if used in PowerShell

    content_table = extract_cegep(file_path)
    

    generate_order(content_table)
    generate_ISBN(content_table)

    print()
    print("===============================================")
    print("Commande généré avec succès.")
    print("===============================================")
    if alert:
        print()
        print("===============================================")
        print("***ISBN DIFFÉRENTS, VÉRIFIEZ LE ISBN NOTÉ D'UNE ÉTOILE DANS cegep_vente.txt***")
        print("===============================================")
    input("Appuyez sur ENTER pour quitter...")
    # for row in order_table:
    #     print(row)

def normalize_path(p):
    p = p.strip()
    if p.startswith("& '") and p.endswith("'"):
        return p[3:-1]
    return p


#this function will go through the text file and methodically extract the relevant information
#It will return a table containing the extracted information
def extract_cegep(file_path):
    with open(file_path, "r", encoding="cp1252") as file:
        content_table = []
        
        content = file.read()

        #split the text where the split_word is
        split_word = "BON DE COMMANDE # "
        split = content.split(split_word)

        for index, part in enumerate(split):

            if index == 0: #Skip the bit before we get actual information
                continue
            content_row = []
            
            content_row.append(part[:14])

            part = part.split("1. Exemplaires:")
            content_row.append(part[1][:3].replace(" ", ""))

            part = part[1].split("Prix unitaire:$")
            content_row.append(part[1][:10].replace(" ", ""))

            part = part[1].split("prix total:$")
            content_row.append(part[1][:10].replace(" ", ""))

            part = part[1].split("ISBN/ISSN:")
            content_row.append(part[1][:15].replace(" ", ""))

            if "Auteur:" in part[1]:
                part = part[1].split("Auteur:")
                content_row.append(part[1].split("\n", 1)[0])
            else:
                content_row.append("")

            if "Titre:" in part[1]:
                part = part[1].split("Titre:")
                content_row.append(part[1].split("\n", 1)[0])
            else:
                content_row.append("")
            
            if "ISBN:" in part[1]:
                part = part[1].split("ISBN:")
                isbn_line = part[1].split(" ", 1)[0]
                content_row.append("".join(c for c in isbn_line if c.isdigit()))
            else:
                content_row.append("")
            
            # for i,p in enumerate(part):
            #     print(i, " *:* ", p)
            #if there is more than one ISBN 
            if len(part) > 2:
                isbn_line = part[2].split(" ", 1)[0]
                content_row.append("".join(c for c in isbn_line if c.isdigit()))
                part[1] = part[2]
            else:
                content_row.append("")

            if "Editeur:" in part[1]:
                part = part[1].split("Editeur:")
                content_row.append(part[1].split("\n", 1)[0])
            else:
                content_row.append("")
            
            print(content_row)
            content_table.append(content_row)
            
            

    return content_table



def generate_order(content_table):
    order_table = []
    for row in content_table:
        order_row = []

        #verify and add the ISBN, add * if unsure
        if row[4] != row[7]:
            order_row.append("*" + row[4])
            global alert
            alert = True
        else:
            order_row.append(row[4])
        
        #add the quantity
        order_row.append(row[1])
        #add the order code

        order_row.append(row[0])

        order_table.append(order_row)


    #part 2 write in a brand new doc the formated output
    #with open(OUTPUT_ORDER, "w", encoding="utf-8") as output_file:
    with open(config.OUTPUT_ORDER_CEGEP, "w", encoding="utf-8") as output_file:
        for row in order_table:
            output_file.write("\t".join(row) + "\n")
    #return order_table

def generate_ISBN(content_table):
    order_table = []
    for row in content_table:
        order_table.append(row[4])

    #part 2 write in a brand new doc the formated output
    with open(config.OUTPUT_LIST_CEGEP, "w", encoding="utf-8") as output_file:
    #with open(OUTPUT_LIST, "w", encoding="utf-8") as output_file:
        for row in order_table:
            output_file.write(row + "\n")

if __name__ == "__main__":
    read_cegep()