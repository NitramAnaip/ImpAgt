# Import bibs
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup 
import requests


# Load driver (for Google Chrome)  
chromedriver = "/usr/local/bin/chromedriver"
os.environ["webdriver.chrome.driver"] = chromedriver
driver = webdriver.Chrome(chromedriver)

url = "https://bib.cnrs.fr/#"
ID = "18CHIMFR3417"
mdp = "MSSLPT"
ressource_type = "article"
keywords = "agriculture technology"

driver.get(url)

# Authentification
connexion = driver.find_element_by_xpath('/html/body/header/div[2]/div[1]/div/div/button').click()
via_code = driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/div/div[2]/button[2]').click()

# Put a wait time because the window hasn't poped up yet
driver.implicitly_wait(5)
login = driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/div/div[2]/div/div/div/input[1]')
login.send_keys(ID)
password = driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/div/div[2]/div/div/div/input[2]')
password.send_keys(mdp)
connect = driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/div/div[2]/div/div/div/button').click()

# Select if you want to search for books or articles
if ressource_type=="article":
    article = driver.find_element_by_xpath('/html/body/div[1]/div[1]/div/div/nav/div/ul/li[1]/a').click()
elif ressource_type=="book":
    book = driver.find_element_by_xpath('/html/body/div[1]/div[1]/div/div/nav/div/ul/li[2]').click()

# Search for ressources using keywords
search = driver.find_element_by_xpath('/html/body/div[1]/div[1]/div/div/div/div[1]/div/div[1]/span/div/div[1]/span/div/input')
search.send_keys(keywords)
search.send_keys(Keys.ENTER)

# this is just to ensure that the page is loaded 
driver.implicitly_wait(10)

# Take to driver directly to the search-results path
search_result = driver.find_element_by_xpath('/html/body/div[1]/div[1]/div/div/div/span/div/div[2]')

# It renders the JS code and stores all of the information in static HTML code
html = driver.page_source

# Now, we can simply apply bs4 to html variable 
soup = BeautifulSoup(html, "html.parser")

# Extract links
ressources_links = soup.select("div.record.record-article [href]")
links = []
for ressource in ressources_links : 
    links.append(ressource['href'])
    print(ressource['href'])
  
driver.quit() # closing the webdriver 