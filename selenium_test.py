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
        access_isbn()

    driver.quit()

def access_isbn():

    isbn = input("Please enter an ISBN : ")

    driver.get(f"https://www.mementolivres.com/viewtitle.aspx?ean={isbn}")
    
    #get the content of <div class="main-title">
    #                        the title is here
    #                   </div>
    #And replace the driver.title with it
    title_element = wait.until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, ".main-title"))
    )

    print("Page title:", title_element.text)

    

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