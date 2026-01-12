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

    detected_error = False
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
                words = line[1:].split()
                word_index = 0
                
                #In case there is no author
                if words[0].isdigit() and len(words[0]) == 13:
                    order_row.append("") #Column 0
                    word_index = 0 #Current location is on the ISBN
                    
                else: #If there is an author
                    combined_authors = ""
                    for i, word in enumerate(words):
                        
                        #Once the ISBN is reached get out of the loop
                        if word.isdigit() and len(word) == 13:
                            word_index = i
                            break
                        
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
                

                
                
                line_number = 2
                    

            elif line_number == 2:
                order_row.append(line) #Column 4 (Title)
                line_number = 3

            elif line_number == 3: #This line is kinda useless, QTY * unit price give the same result
                line_number = 1
                print(order_row)
                order_table.append(order_row)
                order_row = []
                

            
            
            #break



def generate_order(content_table):
    pass

def generate_ISBN(content_table):
    pass

if __name__ == "__main__":
    read_bdg()