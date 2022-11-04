import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
import urllib.parse
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
import getpass


DRIVER_LOCATION = "path/to/driver"
SEARCH_LINKEDIN_URL = "url to what you searched on LinkedIn"

def get_contact_info(contact_driver):
    """Get contact info from the contact URL in the LI profile.
    
    Args:
        contact_driver: The driver of the contact.
        platform: '@' (for email), 'facebook', 'twitter', or website.

    Returns:
        The contact info (email or social medial link).    
    """
    # TODO: iterate to get social media account & to return all
    # (not just a single contact info like the email)
    try:
        site = contact_driver.find_element_by_xpath('.//a[@class="pv-contact-info__contact-link link-without-visited-state"]').text.strip()
    except NoSuchElementException:
        return None
    if site is None:
        return None
    return site

def get_driver(headless=False):
    options = Options()
    if headless:
        options.add_argument("--headless")
    return webdriver.Firefox(DRIVER_LOCATION, options=options)

def sign_in(driver):
    url = "https://www.linkedin.com/uas/login"
    driver.get(url)
    time.sleep(3)
    email = driver.find_element_by_id("username")
    email.send_keys(os.environ['USERNAME'])
    password = driver.find_element_by_id("password")
    password.send_keys(getpass.getpass())
    time.sleep(1)
    password.send_keys(Keys.RETURN)
    time.sleep(2)
    print("Signed in successfully!")

if __name__ == "__main__":
    driver = get_driver()
    sign_in(driver)

    # search for specifics
    time.sleep(1)
    search_url = SEARCH_LINKEDIN_URL
    decoded_url = urllib.parse.unquote(search_url)
    s_arr = decoded_url.split('&sid')

    firstnames = []
    lastnames = []
    linkedin_urls = []
    sites = []

    driver.get(search_url)
    entities = driver.find_elements_by_xpath("//div[@class='t-roman t-sans']")
    next_button = 1
    page = 1
    while next_button:
        for i in range(len(entities)):
            print("______________________________________________________________")
            print(f"Getting website #{i+1} on page #{page}....")
            entities = driver.find_elements_by_xpath("//div[@class='t-roman t-sans']")
            # use wait with visibility_of_element_located instead of sleep.wait()
            # to avoid staleness b/c the next iterations the DOM is re-loaded &
            # you might not find the element anymore which causes the error of 
            # selenium.common.exceptions.StaleElementReferenceException
            # similar: https://stackoverflow.com/a/59132328/4604121
            
            # print(f"Current url 1: {driver.current_url}")
            try:
                link = entities[i].find_element_by_xpath(".//a[@class='app-aware-link']")  
            except StaleElementReferenceException:
                # https://www.softwaretestingmaterial.com/stale-element-reference-exception-selenium-webdriver/
                wait = WebDriverWait(entities[i], 10)
                link = wait.until(EC.visibility_of_element_located((By.XPATH, ".//a[@class='app-aware-link']"))).get_attribute("value")
            

            # link = entity.find_element_by_xpath(".//div[@class='t-roman t-sans']//a[@class='app-aware-link']")
            name = link.text.strip()
            if name == "LinkedIn Member":
                continue
            name = name.split('View')[0]
            print(f"Name: {name}")
            firstname = name.split(' ')[0]
            lastname = name.split(' ')[1]
            
            link = link.get_attribute('href').split('?')[0]
            contact_url = link + "/overlay/contact-info/"
            driver.get(contact_url)
            # print(f"Current url 2: {driver.current_url}")
            site = get_contact_info(driver)
            print(f"Website is: {site}")
            # Go back, src: https://stackoverflow.com/a/27628410/4604121
            # driver.execute_script("window.history.go(-1)")
            driver.back()
            time.sleep(1)
            linkedin_urls.append(link)
            firstnames.append(firstname)
            lastnames.append(lastname)
            sites.append(site)
        try:
            # //button[@aria-label='Next']
            next_button = driver.find_element_by_xpath("//button[@class='artdeco-pagination__button artdeco-pagination__button--next artdeco-button artdeco-button--muted artdeco-button--icon-right artdeco-button--1 artdeco-button--tertiary ember-view']")
            print(f"Next button: {next_button}")
            next_button.click()
            print(f"Next button is clicked: {next_button}")
            page += 1
        except NoSuchElementException:
            # NEXT: See why it throws this exception after the 1st iteration
            print(f"Next button has not appeared: {next_button}")
            next_button = 0
        file = pd.DataFrame({
        'FirstName': firstnames,
        'LastName': lastnames,
        'Website': sites,
        'Linkedin': linkedin_urls
        })

        file.to_csv(f'data/leads_page{page}.csv', index=False)
    driver.quit()
