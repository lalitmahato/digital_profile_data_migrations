import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.chrome.service import Service
from helper import *


# uncomment driver
s = Service("../drivers/chromedriver_linux64/chromedriver") # add the path of the driver
driver = webdriver.Chrome(service=s)


# click on show more btn
def get_url(url):
    driver.get(url)
    time.sleep(5)

def show_more_btn():
    show_more = driver.find_element(By.CLASS_NAME, 'Buttons__Button-sc-19xdot-1')
    show_more.click()

def to_bs4_object(html_page):
    soup = BeautifulSoup(html_page, "html.parser")
    return soup

# Return the current url html code
def get_page_source():
    result = driver.page_source
    soup = to_bs4_object(result)
    return soup

def submit_form():
    submit = driver.find_element(By.ID, 'submit-form')
    submit.click()

def fill_form(form_name, data):
    # fill the form
    input = driver.find_element(By.NAME, form_name)
    input.clear()
    input.send_keys(data)

def select_dropdown(form_name, data):
    # select the dropdown
    select = Select(driver.find_element(By.NAME, form_name))
    select.select_by_visible_text(data)

def select_radio_btn(form_name):
    radio_btn = driver.find_element(By.NAME, form_name)
    radio_btn.click()

def click_btn_xpath(value):
    btn = driver.find_element(By.XPATH, value)
    btn.click()

def select_by_xpath(xpath, value):
    select = Select(driver.find_element(By.XPATH, xpath))
    select.click()
    radio_btn = driver.find_element(By.NAME, value)



form_url = 'http://ee.kobo.local/x/2eyzRNLp'

get_url(form_url)

columns = ['',]




