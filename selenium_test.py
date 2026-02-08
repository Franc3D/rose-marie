import password
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def web_scraper():
    options = Options()
    options.binary_location = "/usr/bin/chromium-browser"

    options.add_argument("--headless=new") #run without a visible window
    options.add_argument("--no-sandbox") #run without the sandbox layer
    options.add_argument("--disable-dev-shm-usage") #don’t try to use GPU acceleration
    options.add_argument("--disable-gpu") #don’t use /dev/shm for shared memory
    options.add_argument("user-agent=Mozilla/5.0")

    #options.add_argument("--remote-debugging-port=9222") #open a debugging port so ChromeDriver can talk to Chrome
    #options.add_argument("--disable-software-rasterizer")

    global driver
    global wait

    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 10)

    #driver.get("google.com")

    login()

    print("Page title:", driver.title)

    while True:
        access_isbn_page()

    driver.quit()

def access_isbn_page():

    isbn = input("Please enter an ISBN : ")

    driver.get(f"https://www.mementolivres.com/viewtitle.aspx?ean={isbn}")
    
    #get the content of <div class="main-title">
    #                        the title is here
    #                   </div>

    #TITLE
    title_element = wait.until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, ".main-title"))
    )

    #AUTHORS
    contributors = driver.find_elements(By.CSS_SELECTOR, ".mem-contributor-name a") #In this case it will look for any <a> inside the <div class=mem-contributor-name...>
    #Turn it into a list
    authors = [c.text.strip() for c in contributors]

    #for the Série, collection and editor
    mem_label = driver.find_elements(By.CSS_SELECTOR, ".mem-label")
    mem_content = driver.find_elements(By.CSS_SELECTOR, ".mem-series-content a")

    label = [l.text.strip() for l in mem_label]
    content = [c.text.strip() for c in mem_content]

    serie = ""
    collection = ""
    editor = ""

    for x,l in enumerate(label):
        if l == "Série :":
            serie = content[x]
        elif l == "Collection :":
            collection = content[x]
        elif l == "Marque :":
            editor = content[x]
        else:
            print("***Unknown datatype found named as : ", label)

    #extract the number from the serie for better storage
    if len(serie) > 0:
        serie_number = serie.split()[-1]
        serie = serie[:(len(serie_number)+2)*-1]
    else:
        serie_number = ""
    

    #Extract the link of the coverpicture
    coverpicture = driver.find_element(By.CSS_SELECTOR, ".viewtitle-cover-block a")
    coverpicture_url = coverpicture.get_attribute("href")

    
    
    
    #extract the left side of the webpage
    left_panel = driver.find_element(By.CSS_SELECTOR, ".left-collapse-block")
    
    #Next up we need to divide each accordion into 
    segments = left_panel.find_elements(By.CSS_SELECTOR, ".accordion-segment")
    #Yoink the name of the segment from the <h4>
    segments_titles = []
    for seg in segments:
        segments_titles.append(seg.find_element(By.TAG_NAME, "h4").text.strip())

    

    print("Page title:", title_element.text)
    print("Authors : ", authors)
    print("Série : ", serie)
    print("Collection : ", collection)
    print("Éditeur : ", editor)
    print("Numéro de Série : ", serie_number)
    print("Cover image URL : ", coverpicture_url)
    print(left_panel.text)


    

def login():
    driver.get("https://www.mementolivres.com/Login.aspx")

    #within the login form
    form = wait.until(
        EC.presence_of_element_located((By.ID, "frmLoginPage"))
    )


    courriel_box = form.find_element(By.ID, "txtEmail")
    password_box = form.find_element(By.ID, "pasPassword")


    courriel_box.clear()
    password_box.clear()

    courriel_box.send_keys(password.COURRIEL_LOGIN)
    password_box.send_keys(password.PASSWORD_LOGIN)

    login_button = form.find_element(By.ID, "btnLogin")
    
    login_button.click()

    #Verify if the account-menu hs appeared
    account_element = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".logged-in"))
    )
    if EC.url_to_be("https://www.mementolivres.com/SearchResults.aspx?adv=1"):
        print("Login seems successful.")
    else:
        print("Somethin' wonky goin' on!")



    #In case of no ID for button
    #login_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))

if __name__ == "__main__":
    web_scraper()

#1. NAVIGATION
    #-------------------------------------
    #driver.get("https://www.google.com")

    #2. LOCATING ELEMENTS
    #-------------------------------------
    #Using By. to get an element
    #email_box = wait.until(EC.presence_of_element_located((By.ID, "email")))
    #By.ID
    #By.NAME
    #By.CSS_SELECTOR
    #By.XPATH
    #...

    #3 INTERACTING
    #-------------------------------------
    #email_box.send_keys("my_email")
    #password_box.send_keys("my_password")
    #login_button.click()

    #login()