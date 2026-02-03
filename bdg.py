from PyPDF2 import PdfReader
import config

alert = False
alert_message = []

def read_bdg(filepath = ""):
    print()
    print("PROGRAMME D'EXTRACTION DU BON DE COMMANDE DE LA BIBLIO DE GATINEAU")
    print("===============================================")
    print("VEUILLEZ DÉPOSER UN FICHIER À EXTRAIRE")
    print("===============================================")
    print()

    if filepath != "":
        file_path = filepath #import the filepath from main.py
    else:
        file_path = input("Déposez le fichier dans le fenêtre ou inscrivez le chemin du fichier à traiter : ")
        file_path = normalize_path(file_path) #Fixes the filepath if used in PowerShell

    content_table = extract_bdg(file_path)

    generate_order(content_table)
    generate_ISBN(content_table)

    print()
    print("===============================================")
    print("Commande généré avec succès.")
    print("===============================================")
    if alert:
        print()
        print("===============================================")
        for e in alert_message:
            print(e)
        print("===============================================")
    input("Appuyez sur ENTER pour quitter...")

def normalize_path(p):
    print("Here is the exact text being handled *** :", p)
    p = p.strip()
    if p.startswith("& '") and p.endswith("'"):
        return p[3:-1]
    elif p.startswith("\"") and p.endswith("\""):
        return p[1:-1]
    return p

def extract_bdg(file_path):
    reader = PdfReader(file_path)

    no_bon_commande = ""
    order_table = []

    for page in reader.pages:
        #split per lines 
        page_text = page.extract_text()
        lines = page_text.splitlines()
        #print(lines[0])

        #Skip the intro segment (grab the no_bon_commande once at least)
        if no_bon_commande == "":
            no_bon_commande = lines[0][-4:]
            #print(no_bon_commande)
        
        index = 0
        delimitation = "----------------"

        #Find the line where the index ends
        index = next((i for i, s in enumerate(lines) if delimitation in s), None)
        if delimitation in lines[index + 1]:
            index += 2
        #print(lines[index]) 

        #Every product uses 3 lines 
        #Divide every line 1 by spaces and look for 13 numbers, next index is QTY and then price
        #line 2 is the full title + " /"
        #line 3 got the total price at the end moderately useful (could always just qty + price)

        line_number = 1
        order_row = []

        for line in lines[index:]:
            

            #Get out once we reach the end
            if delimitation in line:
                break

            #In case of a mistake where a line is incomplete
            if len(line[1:].split()) <= 1 and line_number != 2:
                continue
            
            if line_number == 1:
                words = line.split()
                word_index = 0
                
                #In case there is no author
                if words[0].isdigit() and len(words[0]) == 13:
                    #order_row.append("") #Column 0
                    word_index = 0 #Current location is on the ISBN
                    
                else: #If there is an author
                    combined_authors = ""
                    for i, word in enumerate(words):
                        
                        #Once the ISBN is reached get out of the loop
                        if word.isdigit() and len(word) == 13:
                            word_index = i
                            break
                        
                        #IF I WANT TO FIGURE OUT HOW TO EXTRACT THE INDEX NUMBER IT COULD BE A NICE PUZZLE TO SOLVE
                        # #in case this is the first word of the line and 
                        # index = ""
                        # if combined_authors == "":
                        #     for letter in word:
                        #         if letter.isdigit():
                        #             index += letter
                        #         else:
                        #             order_row.append(index)
                        #             word = word[len(index.strip()):]
                        #             break

                        combined_authors = combined_authors + " " + word
                    order_row.append(combined_authors) #Column 0

                #Get the ISBN
                order_row.append(words[word_index]) #Column 1
                #print(word_index, words)

                if (len(words)- word_index) == 3: #normal qty + price
                    #Get the quantity     
                    word_index += 1
                    order_row.append(words[word_index]) #Column 2

                    #Get the unit price
                    word_index += 1
                    order_row.append(words[word_index]) #Column 3
                
                elif (len(words)- word_index) == 2: #ABNORMAL qty + price (Add TBD to the QTY slot and leave the price overinflated for human analysis)
                    #Get the quantity     
                    word_index += 1
                    order_row.append("TBD") #Column 2

                    #Get the unit price
                    order_row.append(words[word_index]) #Column 3

                    #Get a warning at the end
                    global alert 
                    global alert_message

                    alert = True
                    alert_message.append("LA QUANTITÉ N'A PAS PU ÊTRE AJOUTÉ CORRECTEMENT " + order_row[1] + " , LA QUANTITÉ POURRAIT ÊTRE COMBINÉ AU PRIX.")
                    

                
                
                line_number = 2
                    

            elif line_number == 2:
                order_row.append(line) #Column 4 (Title)
                line_number = 3

            elif line_number == 3: #This line is kinda useless, QTY * unit price give the same result
                line_number = 1
                print(order_row)
                order_table.append(order_row)
                order_row = []
                

            
    return order_table



def generate_order(content_table):
    order_table = []
    for row in content_table:
        order_row = []
        
        #add the ISBN
        order_row.append(row[1])
        #add the Price
        order_row.append(row[3])
        #add the QTY
        order_row.append(row[2])

        order_table.append(order_row)

        #part 2 write in a brand new doc the formated output
    #with open(OUTPUT_ORDER, "w", encoding="utf-8") as output_file:
    with open(config.OUTPUT_ORDER_BDG, "w", encoding="utf-8") as output_file:
        for row in order_table:
            output_file.write("\t".join(row) + "\n")
    #return order_table

def generate_ISBN(content_table):
    order_table = []
    for row in content_table:
        order_table.append(row[1])

    #part 2 write in a brand new doc the formated output
    with open(config.OUTPUT_LIST_BDG, "w", encoding="utf-8") as output_file:
    #with open(OUTPUT_LIST, "w", encoding="utf-8") as output_file:
        for row in order_table:
            output_file.write(row + "\n")

if __name__ == "__main__":
    read_bdg()