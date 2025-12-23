#This is the project for Rose-Marie
#Starting with the cegep .txt files
#import pygame


def main():
    text = extract_cegep("cegep_commande.txt")
    


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
            


            #print("****", part[1])


            print("***", content_row)
            #print("****", part[1])

    return content


if __name__ == "__main__":
    main()