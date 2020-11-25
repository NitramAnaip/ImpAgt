from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from bs4 import BeautifulSoup 

def authentificate(driver_sel,login,password):
    # Authentification
    connexion = driver_sel.find_element_by_class_name("login-button.btn.btn-link").click()
    via_code = driver_sel.find_element_by_class_name("inist-button.btn.btn-primary.btn-block").click()

    # Put a wait time because the window hasn't popped up yet
    driver_sel.implicitly_wait(5)
    login_input = driver_sel.find_element_by_class_name('username.form-control')
    login_input.send_keys(login)
    password_input = driver_sel.find_element_by_class_name('password.form-control')
    password_input.send_keys(password)
    connect = driver_sel.find_element_by_class_name('fetch-button.api.btn.btn-primary.btn-block').click()


def search_ressource(driver_sel,ressource_type,keywords):
    # Select if you want to search for books or articles
    if ressource_type=="article":  
        article = driver_sel.find_element_by_class_name('nav-item.nav-article.active').click()
        search = driver_sel.find_element_by_class_name('form-control')
    elif ressource_type=="book":
        book = driver_sel.find_element_by_class_name('nav-item.nav-publication').click()
        search = driver_sel.find_element_by_class_name('form-control')
    
    # Search for ressources using keywords
    search.send_keys(keywords)
    search.send_keys(Keys.ENTER)

def select_date(driver_sel, date_from, date_to):
    date_start = driver_sel.find_element_by_class_name('from')
    date_start.clear()
    date_start.send_keys(date_from)

    date_start = driver_sel.find_element_by_class_name('to.btn.form-control')
    date_start.clear()
    date_start.send_keys(date_to)

    apply_filter = driver_sel.find_element_by_class_name('fetch-button.title.clearFacet.btn.btn-primary')
    driver_sel.execute_script("arguments[0].click();", apply_filter)


def article_source(soup):
    type_publication = soup.find('dt',text='Type of publication')
    publisher = soup.find('dt',text='Publisher')
    document_type = soup.find('dt',text='Document type')

    if publisher != None:
        source = publisher.find_next("span").text
        return source

    elif type_publication != None:
        type_publication = type_publication.find_next("span").text

        if type_publication.lower() == 'journal paper':
            source = soup.find('dt',text='Source').find_next("span").text
            source = source.split('Publisher:')[1].split('Country')[0]
            return source

    elif document_type != None:
        document_type = document_type.find_next("span").text.lower()
        if (document_type == 'working paper') | (document_type == 'report'):
            return 'arxiv'

    return 'unknown'