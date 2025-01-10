import csv
from bs4 import BeautifulSoup
import re
import random
import string

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def scrap(driver):
    
 # Attendre que la page soit complètement chargée
    wait = WebDriverWait(driver, 10)  # Attendre jusqu'à 10 secondes
# Attendre que le tag 'body' soit présent :
    wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

    print(f"La page {driver.current_url} a complètement chargé.")

    content = driver.page_source
    soup = BeautifulSoup(content, 'lxml')