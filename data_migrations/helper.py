import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.chrome.service import Service

# Remove Character from the text
def Remove_Character(Text, characters):
    val = Text.get_text(separator=' ').rstrip().split()
    val = ' '.join(val)
    for c in characters:
        val = ''.join(val.split(c))
    return val

# Get the position value
def Get_Position_Value(Text_Value, value_address):
    val = Text_Value.get_text(separator=' ').rstrip().split()
    return(val[value_address])

# Join the array with given tag
def Join_Value_With(value, join_value):
    val = value.get_text(separator=' ').rstrip().split()
    val = join_value.join(val)
    return(val)

# To Reamove Unusal Spaces
def Remove_Unusal_Spaces(value):
    try:
        val = value.get_text(separator=' ').rstrip().split()
        val = ' '.join(val)
    except:
        val = ''
    return(val)

# Make the attributes naming 
def Name_Attribute(attribute):
    """remove the unusual spaces and convert the sentence into array"""
    attr = attribute.get_text(separator=' ').rstrip().split()
    attr = [x.casefold() for x in attr] # capitalize the first letter of the word
    attr = '_'.join(attr) # Join each word with "_"
    return(attr)

def Get_href(anchor):
    """scrap the anchor tag href"""
    href =  anchor.find('a', href=True)['href']
    return href
