# Import bibs
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from bs4 import BeautifulSoup 
import requests


# Load driver (for Google Chrome)  
chromedriver = "/usr/local/bin/chromedriver"
os.environ["webdriver.chrome.driver"] = chromedriver
driver = webdriver.Chrome(chromedriver)

url = "https://bib.cnrs.fr/#"
ID = "18CHIMFR3417"
mdp = "MSSLPT"
ressource_type = "book"
keywords = "technologie"

driver.get(url)

# Authentification
connexion = driver.find_element_by_class_name("login-button.btn.btn-link").click()
via_code = driver.find_element_by_class_name("inist-button.btn.btn-primary.btn-block").click()

# Put a wait time because the window hasn't poped up yet
driver.implicitly_wait(5)
login = driver.find_element_by_class_name('username.form-control')
login.send_keys(ID)
password = driver.find_element_by_class_name('password.form-control')
password.send_keys(mdp)
connect = driver.find_element_by_class_name('fetch-button.api.btn.btn-primary.btn-block').click()
driver.implicitly_wait(10)

# Select if you want to search for books or articles
if ressource_type=="article":  
    article = driver.find_element_by_class_name('nav-item.nav-article.active').click()
    search = driver.find_element_by_class_name('form-control')
elif ressource_type=="book":
    book = driver.find_element_by_class_name('nav-item.nav-publication').click()
    search = driver.find_element_by_class_name('form-control')
    
# Search for ressources using keywords
search.send_keys(keywords)
search.send_keys(Keys.ENTER)

# this is just to ensure that the page is loaded 
driver.implicitly_wait(10)

# Number of links extracted
n_links = 0

# Set current page
current_page = 1

while True:
    # Take to driver directly to the search-results path
    search_result = driver.find_element_by_class_name('search-result')

    try:
        record_list = driver.find_element_by_class_name("record_list")
    except NoSuchElementException:
        print('No result found...')
        break

    # It renders the JS code and stores all of the information in static HTML code
    html = driver.page_source

    # Now, we can simply apply bs4 to html variable 
    soup = BeautifulSoup(html, "html.parser")

    # Condition to stop (if the next page is the same)
    page = int(soup.select("span.current.page")[0].text)
    if (page != current_page):
        end_message = "Last page parsed!"
        print(end_message)
        break

    # Extract links
    if ressource_type=="article": ressources_links = soup.select("div.record.record-article [href]")
    elif ressource_type=="book": ressources_links = soup.select("div.record.record-publication [href]")
    links = []
    for ressource in ressources_links : 
        links.append(ressource['href'])
        print(ressource['href'])
    n_links += len(ressources_links)

    # Next page
    pagination = driver.find_element_by_class_name("pagination")
    next_page = driver.find_element_by_class_name("next").click()
    current_page+=1

print('Number of links extracted : {}'.format(n_links))
driver.quit() # closing the webdriver 