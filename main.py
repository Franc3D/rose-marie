#This is the project for Rose-Marie
#Starting with the cegep .txt files
#import pygame


def main():
    print("PROGRAMME D'EXTRACTION DU BON DE COMMANDE DU CÉGEP")
    print("===============================================")
    print("VEUILLEZ DÉPOSER UN FICHIER À EXTRAIRE")

    file_path = input("Chemin du fichier : ")

    content_table = extract_cegep(file_path)
    

    generate_order(content_table)
    generate_ISBN(content_table)

    print("===============================================")
    print("Commande généré avec succès.")
    input("Appuyez sur n'importe quel bouton pour quitter...")
    # for row in order_table:
    #     print(row)


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

            if index == 0:
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
                isbn_line = part[1].split("\n", 1)[0]
                content_row.append("".join(c for c in isbn_line if c.isdigit()))
            else:
                content_row.append("")
            
            #if there is more than one ISBN
            if len(part) > 2:
                isbn_line = part[2].split("\n", 1)[0]
                content_row.append("".join(c for c in isbn_line if c.isdigit()))
                part[1] = part[2]
            else:
                content_row.append("")

            if "Editeur:" in part[1]:
                part = part[1].split("Editeur:")
                content_row.append(part[1].split("\n", 1)[0])
            else:
                content_row.append("")
            

            content_table.append(content_row)
            
            

    return content_table



def generate_order(content_table):
    order_table = []
    for row in content_table:
        order_row = []

        #verify and add the ISBN, add * if unsure
        if row[4] != row[7]:
            order_row.append("*", row[4])
        else:
            order_row.append(row[4])
        
        #add the quantity
        order_row.append(row[1])
        #add the order code
        order_row.append(row[0])

        order_table.append(order_row)


    #part 2 write in a brand new doc the formated output
    with open("cegep_vente.txt", "w", encoding="utf-8") as output_file:
        for row in order_table:
            output_file.write("\t".join(row) + "\n")
    #return order_table

def generate_ISBN(content_table):
    order_table = []
    for row in content_table:
        order_table.append(row[4])

    #part 2 write in a brand new doc the formated output
    with open("cegep_liste.txt", "w", encoding="utf-8") as output_file:
        for row in order_table:
            output_file.write(row + "\n")

if __name__ == "__main__":
    main()