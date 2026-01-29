# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# import time

# def find_url():
#     isbn = input("ISBN: ")

#     search_url = f"https://www.leslibraires.ca/recherche/?isbn={isbn}"

#     options = Options()
#     options.add_argument("--headless=new")  # run without opening a window

#     driver = webdriver.Chrome(options=options)

#     driver.get(search_url)

#     # Wait for JS to finish redirecting
#     time.sleep(3)

#     print("Final URL:", driver.current_url)

#     driver.quit()

#     input("Appuyez sur ENTER pour continuer...")

# if __name__ == "__main__":
#     find_url()


from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--remote-debugging-port=9222")
options.add_argument("--disable-software-rasterizer")

driver = webdriver.Chrome(options=options)

driver.get("https://www.google.com")

print("Page title:", driver.title)

driver.quit()
